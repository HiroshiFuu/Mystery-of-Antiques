import { Store, select } from '@ngrx/store';
import { Component, OnInit, ChangeDetectionStrategy } from '@angular/core';
import { Observable } from 'rxjs';

import {
  routeAnimations,
  selectIsAuthenticated
} from '../../../core/core.module';

import { State } from '../examples.state';

@Component({
  selector: 'frontend-examples',
  templateUrl: './examples.component.html',
  styleUrls: ['./examples.component.scss'],
  animations: [routeAnimations],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ExamplesComponent implements OnInit {
  isAuthenticated$: Observable<boolean>;

  examples = [
    { link: 'todos', label: 'frontend.examples.menu.todos' },
    { link: 'stock-market', label: 'frontend.examples.menu.stocks' },
    { link: 'theming', label: 'frontend.examples.menu.theming' },
    { link: 'crud', label: 'frontend.examples.menu.crud' },
    {
      link: 'simple-state-management',
      label: 'frontend.examples.menu.simple-state-management'
    },
    { link: 'form', label: 'frontend.examples.menu.form' },
    { link: 'notifications', label: 'frontend.examples.menu.notifications' },
    { link: 'elements', label: 'frontend.examples.menu.elements' },
    { link: 'authenticated', label: 'frontend.examples.menu.auth', auth: true }
  ];

  constructor(private store: Store<State>) {}

  ngOnInit(): void {
    this.isAuthenticated$ = this.store.pipe(select(selectIsAuthenticated));
  }
}
