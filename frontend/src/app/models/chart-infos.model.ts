export class ChartInfos {
    name !: string;
    type !: "pie" | "bar" | "radar";
    labels !: string[]; 
    datas !: number[];
    colors !: string[];
}