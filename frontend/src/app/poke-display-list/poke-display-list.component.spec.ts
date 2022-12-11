import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PokeDisplayListComponent } from './poke-display-list.component';

describe('PokeDisplayListComponent', () => {
  let component: PokeDisplayListComponent;
  let fixture: ComponentFixture<PokeDisplayListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PokeDisplayListComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PokeDisplayListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
