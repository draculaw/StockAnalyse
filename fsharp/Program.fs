// Learn more about F# at http://fsharp.net
// See the 'F# Tutorial' project for more help.
//
//# read from start
//# start  http://finance.yahoo.com/q/hp?s=600568.SS
//
//# if the next exist read the next
//# next <a rel="next" href="/q/hp?s=600568.SS&amp;d=3&amp;e=14&amp;f=2015&amp;g=d&amp;a=4&amp;b=18&amp;c=2001&amp;z=66&amp;y=66" data-rapid_p="21">Next</a>
//
//# <body><div><div><table id="yfncsumtab"><tbody><tr><td><table i"yfnc_datamodoutline1"><tbody><tr><td><table><tbody><tr>
//
//# <tr id="yui_3_9_1_9_1428976539885_38"><td class="yfnc_tabledata1" nowrap="" align="right">Apr 13, 2015</td><td class="yfnc_tabledata1" align="right">20.22</td><td class="yfnc_tabledata1" align="right">21.25</td><td class="yfnc_tabledata1" align="right">20.22</td><td class="yfnc_tabledata1" align="right">20.49</td><td class="yfnc_tabledata1" align="right">14,455,400</td><td class="yfnc_tabledata1" align="right">20.49</td></tr>

//    next_url = doc.xpath("//a[@rel='next']")

//    data = doc.xpath("//td[@class='yfnc_tabledata1']/..")

open System
open System.IO
open System.Net
open Microsoft.FSharp.Control.WebExtensions
open System.Xml
open System.Xml.Linq
open System.Xml.XPath
open System.Xml.Serialization
open Microsoft.FSharp.Data

open System.Drawing
open System.Windows.Forms

open System.Windows.Forms.DataVisualization.Charting



let getCodeFromFile(name:string) =
    try
        let content = File.ReadAllLines(name)
        content |> Array.toList        
    with
        | :? System.IO.FileNotFoundException as e -> 
        printfn "exception %s" e.Message; ["empty"]


let filePath = @"stock.csv"
let splitSemicolon (l:string) =
        l.Split(';')

let splitArrayToTuple x =
        match x with 
          | [| a; b; c; d; e; f; g; h |] -> (a, b, c, d, e, f, g, h)
          | _ -> ("0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0")
    
let openFile (name: string) =
        let filepath = "csv/" + name + ".csv"
        try
            let content = File.ReadAllLines(filepath)
            let data = content |> Array.toList
            data             
        with 
            | :? System.IO.FileNotFoundException as e -> printfn "Exception %s" e.Message; ["empty"]
         

let allStockData (code:string) = 
    openFile code
              |> Seq.skip 1
              |> Seq.filter (fun x -> x.Length > 0)
              |> Seq.map splitSemicolon
              |> Seq.filter (fun x -> x.[0].Equals(code))
              //|> Seq.map splitArrayToTuple
              //|> Seq.toArray     


let getPrices (code:string) = 
        allStockData(code)        
            |> Seq.sortBy (fun x -> x.[1])
            |> Seq.map (fun s -> float s.[5])
            

let movingAverage n (prices:seq<float>) =
        prices
            |> Seq.windowed n
            |> Seq.map Array.sum
            |> Seq.map (fun a -> a / float n)

let stddev2 (values:seq<float>) = 
    let avg = Seq.average values
    values
        |> Seq.fold (fun acc x -> acc + (1.0/ float(Seq.length values)) * (x - avg) ** 2.0) 0.0
        |> sqrt

let movingStdDev n (prices:seq<float>) =
    prices 
        |> Seq.windowed n
        |> Seq.map stddev2


let  get_price_data_form (code:string) = 

    //printfn "%A" allStockData.Length
    let priceForm = new Form(Visible = true, Text = "Displaying data in F#", 
                        TopMost = true, Size = Drawing.Size(900, 400))

    let data = new DataGridView(Dock = DockStyle.Fill, Text = "Data grid", 
                Font = new Drawing.Font("Lucida Console", 10.0f), 
                ForeColor = Drawing.Color.DarkBlue)

    do priceForm.Controls.Add(data)  

    let record_data = 
        allStockData(code)
              |> Seq.map splitArrayToTuple
              |> Seq.sortBy (fun (a,b,c,d,e,f,g,h) -> b)
              //|> Seq.toArray              
              
    do data.DataSource <- Seq.toArray record_data 

    do data.Columns.[0].HeaderText <- "Symb"
    do data.Columns.[1].HeaderText <- "Date"
    do data.Columns.[2].HeaderText <- "Open"
    do data.Columns.[3].HeaderText <- "High"
    do data.Columns.[4].HeaderText <- "Low"
    do data.Columns.[5].HeaderText <- "Close"
    do data.Columns.[6].HeaderText <- "Volume"
    do data.Columns.[7].HeaderText <- "Adj Close"
            
    priceForm

let get_bollinger_data ((n:int), (k:float), (code:string)) = 


    let price = getPrices(code)
    
    let ma = movingAverage n price
    
    let ub = movingStdDev n price

    let sp = price |> Seq.skip n

    sp, ma, ub

let get_bollinger_chart (sp:seq<float>, ma:seq<float>, ub:seq<float>, k:float, code:string) =
    let chart = new Chart(Dock = DockStyle.Fill)
    let area = new ChartArea("Main")
    chart.ChartAreas.Add(area)
    chart.Legends.Add(new Legend())
    
    let bollForm = new Form(Visible = true, TopMost = true, 
                    Width = 1400, Height=600)

    do bollForm.Text <- code

    bollForm.Controls.Add(chart)

    let stockPrice = new Series("Stock price")
    do stockPrice.ChartType <- SeriesChartType.Line
    do stockPrice.BorderWidth <- 2
    do stockPrice.Color <- Drawing.Color.DarkKhaki
    chart.Series.Add(stockPrice)
    
    let movingAvg = new Series("Moving Avg.")
    do movingAvg.ChartType <- SeriesChartType.Line
    do movingAvg.BorderWidth <- 2
    do movingAvg.Color <- Drawing.Color.Blue
    chart.Series.Add(movingAvg)

    let upperBand = new Series("upperBand")
    do upperBand.ChartType <- SeriesChartType.Line
    do upperBand.BorderWidth <- 2
    do upperBand.Color <- Drawing.Color.Red
    chart.Series.Add(upperBand)
    
    let lowerBand = new Series("lowerBand")
    do lowerBand.ChartType <- SeriesChartType.Line
    do lowerBand.BorderWidth <- 2
    do lowerBand.Color <- Drawing.Color.Green
    chart.Series.Add(lowerBand)
  
    do ma |> Seq.iter (movingAvg.Points.Add >> ignore)


    Seq.zip ub ma |> Seq.map (fun (a, b) -> b + k * a) |> Seq.iter (upperBand.Points.Add >> ignore)

    Seq.zip ub ma |> Seq.map (fun (a, b) -> b - k * a) |> Seq.iter (lowerBand.Points.Add >> ignore)
    
    do sp  |> Seq.iter (stockPrice.Points.Add >> ignore)  

    bollForm

    
[<EntryPoint>]
let main argv =
    
    printfn "%A" argv

    let code = 
        match argv.Length with
            | 0 -> "000063.SZ"
            | _ -> argv.[0]

    // TODO: download the csv into csv/*.stock
    let sp, ma, ub = get_bollinger_data(100, 2.0, code)
    let form = get_bollinger_chart (sp, ma, ub, 2.0, code)
    // let form = get_price_data_form code
    
    Application.Run(form)
              
              
    0 // return an integer exit code
