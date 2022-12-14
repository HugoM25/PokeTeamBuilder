import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CommandsElementsComponent } from './commands-elements.component';

describe('CommandsElementsComponent', () => {
  let component: CommandsElementsComponent;
  let fixture: ComponentFixture<CommandsElementsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CommandsElementsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CommandsElementsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
