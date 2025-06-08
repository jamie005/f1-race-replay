import { getGreeting } from '../support/app.po';

describe('f1-race-viewer-e2e', () => {

  it('Should be able to load the site', () => {
    cy.visit('/');
  });
});
