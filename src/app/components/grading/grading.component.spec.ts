import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GradingComponent } from './grading.component';

describe('OneComponent', () => {
  let component: GradingComponent;
  let fixture: ComponentFixture<GradingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GradingComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(GradingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
