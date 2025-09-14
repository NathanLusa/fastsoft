/**
 * Exemplos de uso do ComponentRenderer v2.0
 * Demonstra as novas funcionalidades e melhores práticas
 */

// Exemplo 1: Uso básico com validação
function exemploBasico() {
    const jsonData = {
        page: {
            title: "Formulário de Exemplo",
            layout: "max-w-2xl mx-auto p-6",
            components: [
                {
                    type: "h1",
                    content: "Cadastro de Usuário",
                    attributes: {
                        className: "text-center mb-8 text-3xl font-bold",
                    },
                },
                {
                    type: "form",
                    attributes: {
                        className: "space-y-6",
                        method: "post",
                        action: "/submit",
                    },
                    components: [
                        {
                            type: "fieldset",
                            legend: "Dados Pessoais",
                            attributes: {
                                className: "space-y-4",
                            },
                            components: [
                                {
                                    type: "div",
                                    attributes: {
                                        className: "space-y-2",
                                    },
                                    components: [
                                        {
                                            type: "label",
                                            content: "Nome Completo:",
                                            attributes: {
                                                htmlFor: "name",
                                                className: "block text-sm font-medium text-gray-700",
                                            },
                                        },
                                        {
                                            type: "input",
                                            attributes: {
                                                id: "name",
                                                name: "name",
                                                type: "text",
                                                required: true,
                                                maxLength: 100,
                                                className: "w-full px-3 py-2 border border-gray-300 rounded-md",
                                            },
                                        },
                                    ],
                                },
                            ],
                        },
                    ],
                },
            ],
        },
    };

    // Renderizar com validação habilitada
    const renderer = renderComponentsWithValidation(jsonData, "#container", {
        realTimeValidation: true,
        enableAnimations: true,
    });

    return renderer;
}

// Exemplo 2: Uso avançado com callbacks personalizados
function exemploAvancado() {
    const options = {
        enableValidation: true,
        enableAnimations: true,
        debugMode: true,
        onValidSubmit: function ($form) {
            const formData = getFormData($form);
            console.log("Dados do formulário:", formData);

            // Simular envio
            showLoading("Enviando dados...");

            setTimeout(() => {
                hideLoading();
                showSuccess("Formulário enviado com sucesso!");
            }, 2000);
        },
        onError: function (xhr, status, error) {
            console.error("Erro:", error);
            showError("Erro ao carregar formulário");
        },
    };

    // Carregar formulário via AJAX
    loadAndRenderForm("/api/form", "#container", options);
}

// Exemplo 3: Adicionando validadores customizados
function exemploValidadoresCustomizados() {
    const renderer = new ComponentRenderer({
        enableValidation: true,
        debugMode: true,
    });

    // Adicionar validador customizado para CPF
    renderer.addValidator("cpf", function (value) {
        // Validação básica de CPF (apenas formato)
        const cpfRegex = /^\d{3}\.\d{3}\.\d{3}-\d{2}$/;
        return cpfRegex.test(value);
    });

    // Adicionar validador customizado para telefone
    renderer.addValidator("phone", function (value) {
        const phoneRegex = /^\(\d{2}\)\s\d{4,5}-\d{4}$/;
        return phoneRegex.test(value);
    });

    // Adicionar animação customizada
    renderer.addAnimation("slideInLeft", function ($element) {
        $element
            .css({
                transform: "translateX(-100%)",
                opacity: 0,
            })
            .animate(
                {
                    transform: "translateX(0)",
                    opacity: 1,
                },
                500
            );
    });

    return renderer;
}

// Exemplo 4: Trabalhando com formulários dinâmicos
function exemploFormularioDinamico() {
    // Função para adicionar campo dinamicamente
    function adicionarCampo() {
        const $container = $("#campos-dinamicos");
        const index = $container.children().length;

        const novoCampo = {
            type: "div",
            attributes: {
                className: "flex space-x-2 mb-2",
            },
            components: [
                {
                    type: "input",
                    attributes: {
                        name: `campo_${index}`,
                        type: "text",
                        placeholder: `Campo ${index + 1}`,
                        className: "flex-1 px-3 py-2 border border-gray-300 rounded-md",
                    },
                },
                {
                    type: "button",
                    content: "Remover",
                    attributes: {
                        type: "button",
                        className: "px-3 py-2 bg-red-600 text-white rounded-md hover:bg-red-700",
                        onClick: "removerCampo(this)",
                    },
                },
            ],
        };

        const renderer = new ComponentRenderer();
        const $element = renderer.renderComponent(novoCampo);
        $container.append($element);
    }

    // Função para remover campo
    window.removerCampo = function (button) {
        $(button).closest("div").remove();
    };

    // Adicionar campo inicial
    adicionarCampo();
}

// Exemplo 5: Integração com APIs externas
async function exemploIntegracaoAPI() {
    try {
        // Carregar dados de uma API externa
        const response = await fetch("https://jsonplaceholder.typicode.com/users");
        const users = await response.json();

        // Criar lista de usuários
        const userList = {
            type: "div",
            attributes: {
                className: "space-y-4",
            },
            components: users.map((user) => ({
                type: "div",
                attributes: {
                    className: "bg-white p-4 rounded-lg shadow border",
                },
                components: [
                    {
                        type: "h3",
                        content: user.name,
                        attributes: {
                            className: "text-lg font-semibold text-gray-800",
                        },
                    },
                    {
                        type: "p",
                        content: user.email,
                        attributes: {
                            className: "text-gray-600",
                        },
                    },
                    {
                        type: "a",
                        content: "Ver perfil",
                        attributes: {
                            href: `#user/${user.id}`,
                            className: "text-blue-600 hover:text-blue-800 underline",
                        },
                    },
                ],
            })),
        };

        const renderer = new ComponentRenderer({
            enableAnimations: true,
        });

        renderer.renderPage({ page: { components: [userList] } }, "#user-list");
    } catch (error) {
        console.error("Erro ao carregar usuários:", error);
        showError("Erro ao carregar lista de usuários");
    }
}

// Exemplo 6: Validação de formulário com feedback visual
function exemploValidacaoComFeedback() {
    const renderer = new ComponentRenderer({
        enableValidation: true,
        enableAnimations: true,
    });

    // Adicionar validação em tempo real
    $(document).on("input", 'input[type="email"]', function () {
        const $input = $(this);
        const isValid = renderer.validateElement($input, { email: true });

        if (isValid) {
            $input.removeClass("border-red-500").addClass("border-green-500");
        } else {
            $input.removeClass("border-green-500").addClass("border-red-500");
        }
    });

    // Validação de senha com confirmação
    $(document).on("input", 'input[name="password"], input[name="confirm_password"]', function () {
        const password = $('input[name="password"]').val();
        const confirmPassword = $('input[name="confirm_password"]').val();

        if (confirmPassword && password !== confirmPassword) {
            $('input[name="confirm_password"]').addClass("border-red-500");
            $('input[name="confirm_password"]').siblings(".validation-error").remove();
            $('input[name="confirm_password"]').after(
                '<div class="validation-error text-red-600 text-sm mt-1">As senhas não coincidem</div>'
            );
        } else {
            $('input[name="confirm_password"]').removeClass("border-red-500");
            $('input[name="confirm_password"]').siblings(".validation-error").remove();
        }
    });
}

// Exemplo 7: Uso com TypeScript (se disponível)
/**
 * @typedef {Object} ComponentOptions
 * @property {boolean} enableValidation
 * @property {boolean} enableAnimations
 * @property {boolean} debugMode
 * @property {Function} onValidSubmit
 * @property {Function} onError
 */

/**
 * Função tipada para renderizar componentes
 * @param {Object} jsonData - Dados JSON do componente
 * @param {string} targetSelector - Seletor do elemento alvo
 * @param {ComponentOptions} options - Opções de configuração
 * @returns {ComponentRenderer} Instância do renderer
 */
function renderComponentsTyped(jsonData, targetSelector, options = {}) {
    return renderComponents(jsonData, targetSelector, options);
}

// Exemplo 8: Testes unitários (estrutura básica)
function exemploTestes() {
    // Mock do jQuery para testes
    const mockJQuery = {
        find: () => mockJQuery,
        on: () => mockJQuery,
        attr: () => mockJQuery,
        addClass: () => mockJQuery,
        removeClass: () => mockJQuery,
        html: () => mockJQuery,
        text: () => mockJQuery,
        val: () => mockJQuery,
        prop: () => mockJQuery,
        append: () => mockJQuery,
        after: () => mockJQuery,
        siblings: () => mockJQuery,
        children: () => mockJQuery,
        closest: () => mockJQuery,
        is: () => false,
        length: 0,
    };

    // Teste básico de validação
    function testarValidacao() {
        const renderer = new ComponentRenderer();

        // Teste de validação de email
        const emailValidator = renderer.validators.get("email");
        console.assert(emailValidator("test@example.com") === true, "Email válido deve passar");
        console.assert(emailValidator("invalid-email") === false, "Email inválido deve falhar");

        console.log("Testes de validação passaram!");
    }

    // Executar testes
    testarValidacao();
}

// Exemplo 9: Configuração global
function configuracaoGlobal() {
    // Configurar renderer global
    window.componentRenderer = new ComponentRenderer({
        enableAnimations: true,
        enableValidation: true,
        debugMode: false,
    });

    // Adicionar validadores globais
    window.componentRenderer.addValidator("cnpj", function (value) {
        const cnpjRegex = /^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$/;
        return cnpjRegex.test(value);
    });

    // Adicionar animações globais
    window.componentRenderer.addAnimation("pulse", function ($element) {
        $element.addClass("animate-pulse");
        setTimeout(() => $element.removeClass("animate-pulse"), 1000);
    });

    // Configurar callbacks globais
    window.onFormValid = function ($form) {
        console.log("Formulário válido:", getFormData($form));
        showSuccess("Formulário enviado com sucesso!");
    };

    console.log("Configuração global aplicada!");
}

// Exemplo 10: Uso em produção
function exemploProducao() {
    // Configuração para produção
    const configProducao = {
        enableAnimations: true,
        enableValidation: true,
        debugMode: false,
        timeout: 15000,
        errorMessage: "Erro interno do servidor. Tente novamente.",
        showLoading: true,
    };

    // Função para carregar página
    function carregarPagina(url) {
        return loadAndRenderForm(url, "#main-content", configProducao);
    }

    // Função para renderizar componente
    function renderizarComponente(jsonData) {
        return renderComponents(jsonData, "#component-container", configProducao);
    }

    // Expor funções globalmente
    window.carregarPagina = carregarPagina;
    window.renderizarComponente = renderizarComponente;

    console.log("Sistema de produção configurado!");
}

// Inicialização dos exemplos
$(document).ready(function () {
    console.log("ComponentRenderer v2.0 - Exemplos carregados!");

    // Configurar sistema global
    configuracaoGlobal();

    // Exemplo de uso básico
    // exemploBasico();

    // Exemplo de testes
    // exemploTestes();

    // Configurar para produção
    // exemploProducao();
});

