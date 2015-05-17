module CalcIndex

open GetData
         
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
        
let get_bollinger_data ((n:int), (k:float), (code:string)) = 


    let price = getPrices(code)
    
    let ma = movingAverage n price
    
    let ub = movingStdDev n price

    let sp = price |> Seq.skip n

    sp, ma, ub