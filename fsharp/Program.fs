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

open CalcIndex
open CreateForm




    
[<EntryPoint>]
let main argv =
    
    printfn "%A" argv

    let code = 
        match argv.Length with
            | 0 -> "000063.SZ"
            | _ -> argv.[0]


    // TODO: download the csv into csv/*.stock
    
    let form = get_bollinger_chart (100, 2.0, code)
    // let form = get_price_data_form code
    
    Application.Run(form)
              
//              
    0 // return an integer exit code
