module CreateForm

open System
//open System.Drawing
open System.Windows.Forms
open System.Windows.Forms.DataVisualization.Charting

open System.Xml.Serialization
open Microsoft.FSharp.Data

open GetData
open CalcIndex


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


//let get_bollinger_chart (sp:seq<float>, ma:seq<float>, ub:seq<float>, k:float, code:string) =
let get_bollinger_chart ((n:int), (k:float), (code:string)) = 

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
    
    let sp, ma, ub = get_bollinger_data(100, 2.0, code)

    do ma |> Seq.iter (movingAvg.Points.Add >> ignore)


    Seq.zip ub ma |> Seq.map (fun (a, b) -> b + k * a) |> Seq.iter (upperBand.Points.Add >> ignore)

    Seq.zip ub ma |> Seq.map (fun (a, b) -> b - k * a) |> Seq.iter (lowerBand.Points.Add >> ignore)
    
    do sp  |> Seq.iter (stockPrice.Points.Add >> ignore)  

    bollForm