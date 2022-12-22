import { Component } from '@angular/core';
import { SharedServiceService } from '../services/shared-service.service';
import { OnInit } from '@angular/core';
import { Output, EventEmitter, Input } from '@angular/core';
@Component({
  selector: 'app-commands-elements',
  templateUrl: './commands-elements.component.html',
  styleUrls: ['./commands-elements.component.scss']
})

export class CommandsElementsComponent implements OnInit {

  @Output() onGenerate = new EventEmitter<{tier:string}>();

  @Input() availableFormats!: string[];
  
  activeformat!: string;
  
  constructor(private sharedService: SharedServiceService) { 

  }

  ngOnInit(): void {
  }

  generateTeam(){
    this.onGenerate.emit({
      tier : this.activeformat
    });
  }

}
