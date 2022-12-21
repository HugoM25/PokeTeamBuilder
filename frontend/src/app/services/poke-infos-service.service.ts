import { Injectable } from '@angular/core';
import { pokeInfos } from '../models/poke-infos.model';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class PokeInfosServiceService {

  constructor(private http:HttpClient) { }

  //Get the list of pokeInfos from the backend
  getPokeInfosList() : Observable<pokeInfos[]> {
    return this.http.get<pokeInfos[]>('http://127.0.0.1:5000');
  }

  getPokeData(pokeName: string) : Observable<pokeInfos> {
    const body = { name: pokeName };
    const req = this.http.post<pokeInfos>('http://127.0.0.1:5000/get_pkm', body);
    req.subscribe();
    return req;
  }

  getPokeNames():Observable<string[]> {
    const body = { tier : "GEN8OU" };
    const req = this.http.post<string[]>('http://127.0.0.1:5000/get_pkms_in_tier', body);
    req.subscribe();
    return req;
  }

  generateTeam(teamPoke:pokeInfos[]):Observable<pokeInfos[]> {
    const body = { 
      team : teamPoke, 
      format : "GEN8OU"
    };
    console.log(teamPoke[0]);
    const req = this.http.post<pokeInfos[]>('http://127.0.0.1:5000/complete_team', body);
    return req; 
  }


}
