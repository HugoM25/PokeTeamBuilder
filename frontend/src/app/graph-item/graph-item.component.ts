import { Component, Input } from '@angular/core';
import { Chart } from 'chart.js/auto';
import { OnInit, OnChanges } from '@angular/core';
import { ChartInfos } from '../models/chart-infos.model';

@Component({
  selector: 'app-graph-item',
  templateUrl: './graph-item.component.html',
  styleUrls: ['./graph-item.component.scss']
})
export class GraphItemComponent implements OnChanges {
  
  selfChart !: Chart;
  selfName !: string;
  @Input() index !: number;
  @Input() graphInfos !: ChartInfos;

  constructor() { }


  ngOnChanges() {

    //Compose the id of the chart's canvas
    this.selfName = "myChart" + this.index;

    //Check if the canvas is created
    const chartElement = document.getElementById(this.selfName);

    //Loop until the canvas is created
    const checkForElement = setInterval(() => {
      const chartElement = document.getElementById(this.selfName);
      //When the canvas is created, create the chart
      if (chartElement) {


        if (this.graphInfos.type == "pie"){
          this.selfChart = new Chart(this.selfName, {
            type: this.graphInfos.type,
            data: {
              labels: this.graphInfos.labels,
              datasets: [
                {
                  data: this.graphInfos.datas,
                  backgroundColor: this.graphInfos.colors,
                }
              ]
            }
          });
        }
        else if (this.graphInfos.type == "bar"){
          this.selfChart = new Chart(this.selfName, {
            type: this.graphInfos.type,
            data: {
              labels: this.graphInfos.labels,
              datasets: [
                {
                  data: this.graphInfos.datas,
                  backgroundColor: this.graphInfos.colors,
                }
              ]
            }
          });
        }
        else if (this.graphInfos.type == "radar"){
          this.selfChart = new Chart(this.selfName, {
            type: this.graphInfos.type,
            data: {
              labels: this.graphInfos.labels,
              datasets: [
                {
                  data: this.graphInfos.datas,
                  backgroundColor: this.graphInfos.colors,
                }
              ]
            },
            options: {
              maintainAspectRatio: true,
              scales: {
                r: {
                  min: 0,
                  max: 200,
                  beginAtZero: true,
                  angleLines: {
                    color: "red",
                 }
               }
              }
            }
          });
        }

    
        // Clear the interval
        
        clearInterval(checkForElement);
      }
    }, 10);

  }
}
