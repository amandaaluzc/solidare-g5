const gerarCpfUnico = () => {
    let cpf = '';
    for (let i = 0; i < 11; i++) {
        cpf += Math.floor(Math.random() * 10);
    }
    return cpf;
};

Cypress.Commands.add('fluxoApadrinhamento', (padrinho) => {
    cy.visit('/');
    cy.contains('button', 'Torne-se padrinho').click();
    cy.url().should('include', '/pagina-exibicao');
    cy.get('#btn-aleatorio').click();
    cy.get('.modal:visible').should('be.visible').find('.btn-apadrinhar').click();
    cy.url().should('include', '/login');
    cy.contains('a', 'Cadastre-se aqui').click();
    cy.url().should('include', '/registrar');

    cy.get('input[name="first_name"]').type(padrinho.firstName);
    cy.get('input[name="last_name"]').type(padrinho.lastName);
    cy.get('input[name="email"]').type(padrinho.email);
    cy.get('input[name="password1"]').type(padrinho.password);
    cy.get('input[name="password2"]').type(padrinho.password);
    cy.get('input[name="telefone"]').type(padrinho.telefone);
    cy.get('input[name="cpf"]').type(padrinho.cpf);
    cy.get('form').submit();
    cy.url().should('include', '/');

    cy.log('Usuário cadastrado, fazendo login para apadrinhar.');
    cy.contains('button', 'Torne-se padrinho').click();
    cy.url().should('include', '/pagina-exibicao');
    cy.get('#btn-aleatorio').click();
    cy.get('.modal:visible').should('be.visible').find('.btn-apadrinhar').click();
    cy.url().should('include', '/login');
    cy.get('input[name="email"]').type(padrinho.email);
    cy.get('input[name="password"]').type(padrinho.password);
    cy.get('form').submit();

    cy.url().should('include', '/pagamento/');
    cy.log('Login bem-sucedido. Redirecionado para o pagamento.');
    cy.get('button.btn-confirmar:visible').first().click();
    cy.get('#modal-confirmacao').should('not.have.class', 'hidden');
    cy.get('#modal-confirmacao form').submit();
    cy.on('window:alert', (text) => {
        expect(text).to.contains('Criança apadrinhada com sucesso');
    });
    cy.url().should('include', '/pagina-exibicao');

    cy.visit('/');
    cy.contains('button', 'Sair').click();
    cy.log(`Padrinho ${padrinho.firstName} deslogado.`);
});

describe('Fluxo E2E Completo: Apadrinhamento e Verificação do Administrador', () => {

    before(() => {
        // Limpa dados
        cy.request('POST', '/teste/limpar-geral/');

        // Login como admin para cadastrar crianças
        cy.visit('/login_admin');
        cy.get('input[name="nome"]').type(Cypress.env('ADMIN_USER'));
        cy.get('input[name="password"]').type(Cypress.env('ADMIN_PASS'));
        cy.get('form').submit();
        cy.url().should('not.include', '/login_admin');

        // Cadastro criança 1
        cy.visit('/criancas/cadastrar/');
        cy.get('input[name="nome"]').type('Ana');
        cy.get('input[name="idade"]').type('7');
        cy.get('select[name="genero"]').select('Feminino');
        cy.get('textarea[name="descricao"]').type('Criança Ana.');
        cy.get('button.btn-cadastrar').click();

        // Cadastro criança 2
        cy.visit('/criancas/cadastrar/');
        cy.get('input[name="nome"]').type('Bruno');
        cy.get('input[name="idade"]').type('9');
        cy.get('select[name="genero"]').select('Masculino');
        cy.get('textarea[name="descricao"]').type('Criança Bruno.');
        cy.get('button.btn-cadastrar').click();

        // Cadastro criança 3
        cy.visit('/criancas/cadastrar/');
        cy.get('input[name="nome"]').type('Carla');
        cy.get('input[name="idade"]').type('12');
        cy.get('select[name="genero"]').select('Feminino');
        cy.get('textarea[name="descricao"]').type('Criança Carla.');
        cy.get('button.btn-cadastrar').click();

        // Logout admin
        cy.visit('/');
        cy.contains('button', 'Sair').click();
    });

    it('Cenário 1: Primeiro padrinho deve cadastrar e apadrinhar uma criança', () => {
        const padrinho1 = {
            firstName: 'João',
            lastName: 'Silva',
            email: `joao.silva.${Date.now()}@email.com`,
            password: 'senhaSegura123!',
            telefone: '11999999999',
            cpf: gerarCpfUnico(),
        };
        cy.fluxoApadrinhamento(padrinho1);
    });

    it('Cenário 2: Segundo padrinho deve cadastrar e apadrinhar outra criança', () => {
        const padrinho2 = {
            firstName: 'Maria',
            lastName: 'Souza',
            email: `maria.souza.${Date.now()}@email.com`,
            password: 'outraSenhaForte456!',
            telefone: '21988888888',
            cpf: gerarCpfUnico(),
        };
        cy.fluxoApadrinhamento(padrinho2);
    });

    it('Cenário 3: Administrador deve logar, editar e excluir um padrinho', () => {
        const username = Cypress.env('ADMIN_USER');
        const password = Cypress.env('ADMIN_PASS');
        const novoNome = 'Pedro Silva';

        cy.visit('/login_admin/');
        cy.get('#nome-login').clear().type(username);
        cy.get('#senha-login').clear().type(password);
        cy.contains('button', 'Entrar').click();
        cy.url().should('include', '/escolha_adm/');
        cy.log('Login do administrador realizado com sucesso.');

        cy.get('a[href="/gerenciar_padrinhos/"]').click();
        cy.url().should('include', '/gerenciar_padrinhos/');
        cy.log('Acessou a página de gerenciamento de padrinhos.');

        cy.get('.edit-button').first().click();
        cy.log('Clicou no botão para editar o primeiro padrinho.');

        cy.get('#editModal').should('be.visible');
        cy.get('#editModal input#nome').clear().type(novoNome);
        cy.get('#editModal button.btn-save').click();
        cy.log(`Nome do padrinho alterado para "${novoNome}".`);

        cy.contains(novoNome).should('be.visible');
        cy.contains('João Silva').should('not.exist');
        cy.log('Verificação concluída: o nome foi atualizado na lista.');

        cy.contains(novoNome).parents('tr').find('button[onclick*="openDeleteConfirmModal"]').click();
        cy.log(`Clicou no botão para deletar o padrinho "${novoNome}".`);

        cy.get('#deleteConfirmModal').should('be.visible');
        cy.get('#deleteConfirmModal .btn-confirm-yes').click();
        cy.log('Confirmou a exclusão.');

        cy.contains(novoNome).should('not.exist');
        cy.log(`Verificação final: Padrinho "${novoNome}" foi removido com sucesso.`);
    });
});
