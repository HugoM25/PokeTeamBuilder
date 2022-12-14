import { Component} from '@angular/core';
import { pokeInfos } from '../models/poke-infos.model';
import { PokeInfosServiceService } from '../services/poke-infos-service.service';
import { Input, OnInit, Output, EventEmitter} from '@angular/core';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-poke-display',
  templateUrl: './poke-display.component.html',
  styleUrls: ['./poke-display.component.scss']
})
export class PokeDisplayComponent implements OnInit {

  //Used to get the pokeInfos from the parent component
  @Input() pokeInfos!: pokeInfos; 

  //Index of position in team list
  @Input() index!: number;

  //Pkm names available choices
  @Input() pokeNamesList!: string[];

  //Used to send data to the parent component
  @Output() pokeNameChange = new EventEmitter<{name:string,index:number}>();


  //Handling the lock button
  locked: boolean = false;
  imageLock : string = "assets/images/lock_icon_open.png";

  //Handling the dropdown menu

  constructor(private pokeInfosService: PokeInfosServiceService) {  }

  ngOnInit(){
    console.log(this.index); 

  }

  //Lock/Unlock the pokemon
  lockPoke() {
    if (this.locked){
      this.imageLock = "assets/images/lock_icon_open.png";
      this.locked = false;
    }
    else {
      this.imageLock = "assets/images/lock_icon_closed.png";
      this.locked = true;
    }
  }

  //Change the pokemon based on the dropdown menu
  setPoke(newEvent: any){
    this.pokeInfos.name = newEvent.target.value;
    this.setPokeParentComponent();
  }

  //Change the pokemon in the parent component
  setPokeParentComponent(){
    this.pokeNameChange.emit({
      name: this.pokeInfos.name,
      index : this.index
    });
  }
}
