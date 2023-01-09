import { Component } from '@angular/core';
import { OnInit } from '@angular/core';
import { ChartInfos } from '../models/chart-infos.model';
import { trigger, state, style, transition, animate, query, stagger, animateChild } from '@angular/animations';

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

  constructor() {}

  ngOnInit(): void {
    // Set up the chart data and options
    this.pieChartInfos = {
      type : "pie",
      labels : ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
      datas : [12, 19, 3, 5, 2, 3],
      colors : ["#FF0000", "#0000FF", "#FFFF00", "#008000", "#800080", "#FFA500"]
    }

    this.barChartInfos = {
      type : "bar",
      labels : ["Red", "Blue"],
      datas : [12, 19],
      colors : ["#FF0000", "#0000FF"]
    }

    this.spiderChartInfos = {
      type : "pie",
      labels : ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
      datas : [12, 19, 3, 5, 2, 3],
      colors : ["#FF0000", "#0000FF", "#FFFF00", "#008000", "#800080", "#FFA500"]
    }
    
    this.chartList = [this.pieChartInfos, this.barChartInfos, this.spiderChartInfos];
  }
}
