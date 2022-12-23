import { Component } from '@angular/core';
import { PokeInfosServiceService } from '../services/poke-infos-service.service';
import { OnInit } from '@angular/core';
import { pokeInfos } from '../models/poke-infos.model';
import { take } from 'rxjs/operators';
import { trigger, state, style, transition, animate, query, stagger, animateChild } from '@angular/animations';

@Component({
  selector: 'app-team-page',
  templateUrl: './team-page.component.html',
  styleUrls: ['./team-page.component.scss'],
  animations: [
    trigger('team', [
      transition(':enter', [
          query('@memberAnimation', [
            stagger(100, [
              animateChild()
            ])
          ])
      ])
  ]),
    trigger('memberAnimation',[
      transition('void => *', [
        style({
            transform: 'translateY(-50%)',
            opacity: 0
        }),
        animate('750ms ease-out', style({
            transform: 'translateY(0)',
            opacity: 1,
        }))
    ])
    ])
  ]
})
export class TeamPageComponent implements OnInit {

  teamList: pokeInfos[] = [];

  
  tiersAvailable: string[] = [];
  tierActive: string = "GEN8OU";
  namesAvailable: string[] = [];

  isLoading: boolean = false;

  //Blank pokemon template
  blankPokeInfos: pokeInfos = {
    id : -1,
    name: "",
    isLocked: false,
    imageUrl : "assets/images/default.png"
  }

  constructor(private pokeInfosService: PokeInfosServiceService){

  }

  ngOnInit(): void {
    //Get the list of pokemon names
    this.resetTeam();
    this.getTiers(); 
    this.setNames();
  }

  //Reset team to blank values
  resetTeam(){
    for (let i = 0; i < 6; i++){
      this.teamList[i] = structuredClone(this.blankPokeInfos);
    }
  }

  //Generate a team in the given tier
  generateTeam(object : {tier:string}){
    this.isLoading = true;
    //Debug
    console.log("generate team");
    console.log(object.tier);
    //Ask backend for a team
    this.pokeInfosService.generateTeam(this.teamList, this.tierActive).pipe(take(1)).subscribe((data:pokeInfos[]) => {
      this.setTeam(data);
      this.isLoading = false;
    });

  }

  //Change the pokemon at index in team 
  changePoke(object: {name:string,index:number}){
    //Shows the desired request
    console.log(object.name);
    console.log(object.index);
    //Execute the request
    this.pokeInfosService.getPokeData(object.name).pipe(take(1)).subscribe((data:pokeInfos) => {
      this.teamList[object.index] = data;
    });
  }
  
  //Lock/Unlock the pokemon at index
  changeLock(object: {locked:boolean,index:number}){
    if (this.teamList[object.index].isLocked){
      this.teamList[object.index].isLocked = false;
    }
    else {
      this.teamList[object.index].isLocked = true;
    }
  }

  setNames(){
    this.pokeInfosService.getPokeNames(this.tierActive).pipe(take(1)).subscribe((data:string[]) => {
      this.namesAvailable = data;
    });
  }

  setTeam(team:pokeInfos[]){
    //Allow to copy attributes of pokemon without changing references
    //This is necessary to avoid component destruction on change
    for (let i = 0; i < 6; i++){
      this.teamList[i] = this.copyMember2(this.teamList[i], team[i]);
    }
  }

  copyMember(member:pokeInfos, memberToCopy:pokeInfos): pokeInfos{
    member.id = memberToCopy.id;
    member.name = memberToCopy.name;
    member.imageUrl = memberToCopy.imageUrl;
    member.isLocked = memberToCopy.isLocked;
    return member;
  }

  copyMember2(member:pokeInfos, memberToCopy:pokeInfos): pokeInfos{
    member = Object.assign(member, memberToCopy);
    return member;
  }

  changeTier(object: {tier:string}){
      this.tierActive = object.tier;
      this.resetTeam();
      this.setNames();
  }

  getTiers(){
    this.pokeInfosService.getTiersNames().pipe(take(1)).subscribe((data:string[]) => {
      this.tiersAvailable = data;
    });
  }
  
}
