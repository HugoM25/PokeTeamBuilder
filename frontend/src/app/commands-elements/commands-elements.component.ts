import { Component } from '@angular/core';
import { OnInit } from '@angular/core';
import { Output, EventEmitter, Input } from '@angular/core';
@Component({
  selector: 'app-commands-elements',
  templateUrl: './commands-elements.component.html',
  styleUrls: ['./commands-elements.component.scss']
})

export class CommandsElementsComponent implements OnInit {

  @Output() onGenerate = new EventEmitter<{tier:string}>();

  @Output() onTierChange = new EventEmitter<{tier:string}>();

  @Input() availableTiers!: string[];
  
  @Input() activeTier!: string;

  @Input() isLoadingTeam!: boolean;
  
  constructor() { 

  }

  ngOnInit(): void {
  }

  setTier(newEvent : any){

    this.onTierChange.emit({
      tier : newEvent.target.value
    })
  }

  generateTeam(){
    this.onGenerate.emit({
      tier : this.activeTier
    });
  }

}
