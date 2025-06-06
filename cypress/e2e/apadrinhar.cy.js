describe('História 01: Apadrinhar uma criança', () => {
  it('Cenário 1: Administrador cadastra criança e padrinho a apadrinha', () => {
    // Limpa o sistema
    cy.request('POST', '/teste/limpar-geral/');

    // Login como admin
    cy.visit('/login_admin');
    cy.get('input[name="nome"]').type('Solidareadmin');
    cy.get('input[name="password"]').type('ADM12345');
    cy.get('form').submit();
    cy.url().should('not.include', '/login_admin');

    // Cadastrar criança
    cy.visit('/criancas/cadastrar/');
    cy.get('input[name="nome"]').type('Maria Teste');
    cy.get('input[name="idade"]').type('7');
    cy.get('select[name="genero"]').select('Feminino');
    cy.get('textarea[name="descricao"]').type('Criança cadastrada antes do teste.');
    cy.get('button.btn-cadastrar').click();

    // Verificar cadastro
    cy.visit('/gerenciar_afilhados/');
    cy.contains('Maria Teste').should('exist');

    // Logout admin
    cy.visit('/');
    cy.contains('button', 'Sair').click();

    // Início do fluxo de apadrinhamento
    cy.visit('/');
    cy.contains('button', 'Torne-se padrinho').click();
    cy.url().should('include', '/pagina-exibicao');

    // Seleciona a criança cadastrada
    cy.contains('.card', 'Maria Teste').click();
    cy.get('.modal:visible').should('be.visible').find('.btn-apadrinhar').click();

    // Redireciona para login
    cy.url().should('include', '/login');

    // Cria nova conta de padrinho
    cy.contains('a', 'Cadastre-se aqui').click();
    cy.url().should('include', '/registrar');

    const email = `teste.${Date.now()}@email.com`;

    cy.get('input[name="first_name"]').type('João');
    cy.get('input[name="last_name"]').type('Silva');
    cy.get('input[name="email"]').type(email);
    cy.get('input[name="password1"]').type('senhaSegura123!');
    cy.get('input[name="password2"]').type('senhaSegura123!');
    cy.get('input[name="telefone"]').type('11999999999');
    cy.get('input[name="cpf"]').type('12345678900');
    cy.get('form').submit();

    // Após cadastro, será redirecionado para a home
    cy.url().should('include', '/');

    // Realiza login novamente (sistema exige)
    cy.visit('/login');
    cy.get('input[name="email"]').type(email);
    cy.get('input[name="password"]').type('senhaSegura123!');
    cy.get('form').submit();
    cy.url().should('include', '/');

    // Refaz o processo de apadrinhar agora logado
    cy.contains('button', 'Torne-se padrinho').click();
    cy.url().should('include', '/pagina-exibicao');

    cy.contains('.card', 'Maria Teste').click();
    cy.get('.modal:visible').should('be.visible').find('.btn-apadrinhar').click();

    // Agora sim vai para o pagamento
    cy.url().should('include', '/pagamento/');
    cy.get('button.btn-confirmar:visible').first().click();

    cy.get('#modal-confirmacao').should('not.have.class', 'hidden');
    cy.get('#modal-confirmacao form').submit();

    cy.on('window:alert', (text) => {
      expect(text).to.contains('Criança apadrinhada com sucesso');
    });

    cy.url().should('include', '/pagina-exibicao');
  });
});
