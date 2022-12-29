import { Component } from '@angular/core';
import { OnInit } from '@angular/core';
import { ChartInfos } from '../models/chart-infos.model';

@Component({
  selector: 'app-stats-page',
  templateUrl: './stats-page.component.html',
  styleUrls: ['./stats-page.component.scss']
})
export class StatsPageComponent {
  
  chartList !: ChartInfos[];

  pieChartInfos !: ChartInfos;
  barChartInfos !: ChartInfos;

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
    
    this.chartList = [this.pieChartInfos, this.barChartInfos];
  }
}
