import { Component } from '@angular/core';
import { pokeInfos } from '../models/poke-infos.model';
import { PokeInfosServiceService } from '../services/poke-infos-service.service';
import { OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { take, map } from 'rxjs/operators';
import { SharedServiceService } from '../services/shared-service.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-poke-display-list',
  templateUrl: './poke-display-list.component.html',
  styleUrls: ['./poke-display-list.component.scss']
})
export class PokeDisplayListComponent implements OnInit{

  pokeInfosList$!: Observable<pokeInfos[]>;

  testOther!: Observable<pokeInfos>;

  pokeInfosList: pokeInfos[] = [];

  public pokeNamesList!: string[]

  clickEventsubscription:Subscription;

  constructor(private pokeInfosService: PokeInfosServiceService, private sharedService:SharedServiceService) { 
    this.clickEventsubscription=    this.sharedService.getClickEvent().subscribe(()=>{
      this.generateTeam();
    });
  }

  //TO DO : check for memory leaks
  
  ngOnInit(): void {
    this.pokeInfosService.getPokeInfosList().pipe(take(1)).subscribe((data:pokeInfos[]) => {
      this.pokeInfosList = data;
      console.log(this.pokeInfosList);

    });
    this.setNames();
  }
  //Change the pokemon at index
  changePoke(object: {name:string,index:number}){
    //Shows the desired request
    console.log(object.name);
    console.log(object.index);
    //Execute the request
    this.pokeInfosService.getPokeData(object.name).pipe(take(1)).subscribe((data:pokeInfos) => {
      this.pokeInfosList[object.index] = data;
    });
  }

  //Lock/Unlock the pokemon at index
  changeLock(object: {locked:boolean,index:number}){
    if (this.pokeInfosList[object.index].isLocked){
      this.pokeInfosList[object.index].isLocked = false;
    }
    else {
      this.pokeInfosList[object.index].isLocked = true;
    }
  }


  setNames(){
    this.pokeInfosService.getPokeNames().pipe(take(1)).subscribe((data:string[]) => {
      this.pokeNamesList = data;
    });
  }
  
  //Generate team 
  generateTeam(){
    this.pokeInfosService.generateTeam(this.pokeInfosList).pipe(take(1)).subscribe((data:pokeInfos[]) => {
      this.pokeInfosList = data;
      console.log(this.pokeInfosList);
    });
  }

  
}
