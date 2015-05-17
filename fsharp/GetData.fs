module GetData


open System
open System.IO
open System.Net
open Microsoft.FSharp.Control.WebExtensions

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
         
let downloadFile (name:string) = 
    async {
        try 
            let uri = new System.Uri("http://104.236.130.177/csv" + name + ".csv")
            let webClient = new WebClient()
            let! html = webClient.AsyncDownloadString(uri)

            let data = 
                let rows = html.Split('\n')
                rows 
                    |> Seq.skip 1
                    |> Seq.toList
            printfn "%A" data
        with 
            | ex -> printfn "Exception %A" ex.Message
    }
    

let allStockData (code:string) = 
    openFile code
              |> Seq.skip 1
              |> Seq.filter (fun x -> x.Length > 0)
              |> Seq.map splitSemicolon
              |> Seq.filter (fun x -> x.[0].Equals(code))


let getPrices (code:string) = 
        allStockData(code)        
            |> Seq.sortBy (fun x -> x.[1])
            |> Seq.map (fun s -> float s.[5])
