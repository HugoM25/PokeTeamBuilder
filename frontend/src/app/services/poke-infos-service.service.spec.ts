import { TestBed } from '@angular/core/testing';

import { PokeInfosServiceService } from './poke-infos-service.service';

describe('PokeInfosServiceService', () => {
  let service: PokeInfosServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PokeInfosServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
