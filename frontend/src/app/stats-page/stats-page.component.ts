import { Component } from '@angular/core';
import { OnInit } from '@angular/core';
import { ChartInfos } from '../models/chart-infos.model';
import { trigger, state, style, transition, animate, query, stagger, animateChild } from '@angular/animations';
import { PokeInfosServiceService } from '../services/poke-infos-service.service';
import { take } from 'rxjs';


@Component({
  selector: 'app-stats-page',
  templateUrl: './stats-page.component.html',
  styleUrls: ['./stats-page.component.scss'],
  animations: [
    trigger('charts', [
      transition(':enter', [
          query('@chartAnim', [
            stagger(100, [
              animateChild()
            ])
          ])
      ])
  ]),
    trigger('chartAnim',[
      transition('void => *', [
        style({
            transform: 'translateY(-50%)',
            opacity: 0
        }),
        animate('500ms ease-out', style({
            transform: 'translateY(0)',
            opacity: 1,
        }))
    ])
    ])
  ]
})
export class StatsPageComponent {
  
  chartList !: ChartInfos[];

  pieChartInfos !: ChartInfos;
  barChartInfos !: ChartInfos;
  spiderChartInfos !: ChartInfos;

  tiersAvailable: string[] = [];
  tierActive: string = "GEN8OU";


  constructor(private pokeInfosService: PokeInfosServiceService) {}

  ngOnInit(): void {
    // Set up the chart data and options
  
    this.pieChartInfos = {
      name : "Pie Chart",
      type : "pie",
      labels : ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
      datas : [12, 19, 3, 5, 2, 3],
      colors : ["#FF0000", "#0000FF", "#FFFF00", "#008000", "#800080", "#FFA500","#FF0000", "#0000FF", "#FFFF00", "#008000", "#800080", "#FFA500","#FF0000", "#0000FF", "#FFFF00", "#008000", "#800080", "#FFA500"]
    }

    this.barChartInfos = {
      name : "Bar Chart",
      type : "bar",
      labels : ["Red", "Blue"],
      datas : [12, 19],
      colors : ["#FF0000", "#0000FF"]
    }

    this.spiderChartInfos = {
      name : "Spider Chart",
      type : "pie",
      labels : ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
      datas : [12, 19, 3, 5, 2, 3],
      colors : ["#FF0000", "#0000FF", "#FFFF00", "#008000", "#800080", "#FFA500"]
    }
  
    this.getTiers();
    //Create list of infos
    this.chartList = [this.pieChartInfos, this.barChartInfos, this.spiderChartInfos];

    this.getInfosOnTier();
  }

  getInfosOnTier(){
        //Get infos for the active tier
        this.pokeInfosService.getStatsTier(this.tierActive).pipe(take(1)).subscribe((data:any) => {
        
        //Update graph of types repartition
        console.log(data["type_repartition"]);
    
        var types_labels : string[] = [];
        var types_datas : number[] = [];
        var types_colors : string[] = [];

        for (let key in data["type_repartition"]){
          types_labels.push(key);
          types_datas.push(data["type_repartition"][key]["nb_pkm"]);
          types_colors.push(data["type_repartition"][key]["color"]);
        }

        this.chartList[0] = {
          name : "Types repartition",
          type : "pie",
          labels : types_labels,
          datas : types_datas,
          colors : types_colors
        }

        //Update graph of average stats 

        var stats_labels : string[] = [];
        var stats_datas : number[] = [];

        for (let key in data["average_stats"]){
          stats_labels.push(key);
          stats_datas.push(data["average_stats"][key]);
        }

        this.chartList[2] = {
          name : "Average stats",
          type : "radar",
          labels : stats_labels,
          datas : stats_datas,
          colors : ["#0000FF"]
        }
        



    });
  }

  getTiers(){
    this.pokeInfosService.getTiersNames().pipe(take(1)).subscribe((data:string[]) => {
      this.tiersAvailable = data;
    });
  }

  setTier(newEvent : any){
    this.tierActive = newEvent.target.value;
    this.getInfosOnTier();

    
  }





}
