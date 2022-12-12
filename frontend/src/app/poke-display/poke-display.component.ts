import { Component} from '@angular/core';
import { pokeInfos } from '../models/poke-infos.model';
import { PokeInfosServiceService } from '../services/poke-infos-service.service';
import { Input, OnInit, Output, EventEmitter} from '@angular/core';


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

  //Used to send data to the parent component
  @Output() pokeNameChange : EventEmitter<string> = new EventEmitter<string>();

  //Contains the choices for the user in the dropdown menu
  pokeNamesList: string[] = [];

  //Handling the lock button
  locked: boolean = false;
  imageLock : string = "assets/images/lock_icon_open.png";

  constructor(private pokeInfosService: PokeInfosServiceService) {  }

  ngOnInit(){
    this.pokeNamesList = this.pokeInfosService.getPokeNames();
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
    this.pokeNameChange.emit(this.pokeInfos.name);
  }
}
