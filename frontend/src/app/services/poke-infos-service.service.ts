import { Injectable } from '@angular/core';
import { PokeInfos } from '../models/poke-infos.model';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class PokeInfosServiceService {

  constructor(private http:HttpClient) { }

  //Get the list of pokeInfos from the backend
  getPokeInfosList() : Observable<PokeInfos[]> {
    return this.http.get<PokeInfos[]>('http://127.0.0.1:5000');
  }

  getPokeData(pokeName: string) : Observable<PokeInfos> {
    const body = { name: pokeName };
    const req = this.http.post<PokeInfos>('http://127.0.0.1:5000/get_pkm', body);
    req.subscribe();
    return req;
  }

  getPokeNames(tier:string):Observable<string[]> {
    const body = { tier : tier };
    const req = this.http.post<string[]>('http://127.0.0.1:5000/get_pkms_in_tier', body);
    req.subscribe();
    return req;
  }

  getTiersNames():Observable<string[]> {
    const req = this.http.get<string[]>('http://127.0.0.1:5000/get_tiers');
    req.subscribe();
    return req;
  }

  generateTeam(teamPoke:PokeInfos[], tier:string):Observable<PokeInfos[]> {
    const body = { 
      team : teamPoke, 
      tier : tier
    };
    const req = this.http.post<PokeInfos[]>('http://127.0.0.1:5000/complete_team', body);
    return req; 
  }

  getCurrentTeamShowdownFormatted(teamPoke:PokeInfos[], tier:string):Observable<string> {
    const body = {
      team : teamPoke,
      tier : tier
    };
    const req = this.http.post<string>('http://127.0.0.1:5000/get_team_showdown_format', body);
    return req; 
  }

  getStatsTier(tier:string):Observable<any> {
    const body = { tier : tier };
    const req = this.http.post<any>('http://127.0.0.1:5000/get_stats_tier', body);
    return req; 
  }
}
