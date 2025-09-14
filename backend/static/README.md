# ComponentRenderer v2.0

## 🚀 Melhorias Implementadas

### ✅ **Novos Componentes Suportados**

-   **Fieldset & Legend**: Para agrupar elementos de formulário
-   **Image**: Componente para imagens com todos os atributos HTML5
-   **Link**: Componente para links (anchor) com atributos de navegação
-   **Heading (h1-h6)**: Componentes para títulos com validação de nível
-   **Paragraph**: Componente para parágrafos de texto

### ✅ **Sistema de Validação Avançado**

-   **Validação em tempo real**: Validação automática ao sair do campo
-   **Validadores customizados**: Adicione seus próprios validadores
-   **Feedback visual**: Indicadores visuais de erro e sucesso
-   **Validação de formulário completo**: Validação de todos os campos de uma vez

### ✅ **Sistema de Animações**

-   **Animações padrão**: fadeIn, slideDown, bounce
-   **Animações customizadas**: Adicione suas próprias animações
-   **Animações de scroll**: Animações baseadas em Intersection Observer
-   **Transições suaves**: Transições CSS integradas

### ✅ **Melhorias de Estrutura**

-   **Código modular**: Estrutura mais limpa e organizada
-   **Configuração flexível**: Opções de configuração extensas
-   **Tratamento de erros**: Sistema robusto de tratamento de erros
-   **Debug mode**: Modo de debug para desenvolvimento

### ✅ **Funcionalidades Utilitárias**

-   **Funções helper**: getFormData, clearForm, showError, showSuccess
-   **Loading states**: Estados de carregamento integrados
-   **Callbacks personalizados**: Callbacks para eventos específicos
-   **API melhorada**: Interface mais intuitiva e poderosa

## 📖 Como Usar

### Uso Básico

```javascript
// Renderizar componentes simples
const renderer = renderComponents(jsonData, "#container");

// Renderizar com validação
const renderer = renderComponentsWithValidation(jsonData, "#container", {
    realTimeValidation: true,
    enableAnimations: true,
});
```

### Uso Avançado

```javascript
// Configuração personalizada
const renderer = new ComponentRenderer({
    enableAnimations: true,
    enableValidation: true,
    debugMode: false,
});

// Adicionar validador customizado
renderer.addValidator("cpf", function (value) {
    const cpfRegex = /^\d{3}\.\d{3}\.\d{3}-\d{2}$/;
    return cpfRegex.test(value);
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
```

### Carregamento via AJAX

```javascript
// Carregar formulário com validação
loadAndRenderForm("/api/form", "#container", {
    enableValidation: true,
    onValidSubmit: function ($form) {
        const data = getFormData($form);
        console.log("Dados:", data);
    },
    onError: function (xhr, status, error) {
        console.error("Erro:", error);
    },
});
```

## 🎨 Componentes Suportados

### Componentes de Formulário

-   `input` - Campos de entrada
-   `select` - Listas de seleção
-   `textarea` - Áreas de texto
-   `button` - Botões
-   `checkbox` - Caixas de seleção
-   `radio` - Botões de rádio
-   `fieldset` - Grupos de campos
-   `legend` - Legendas para grupos

### Componentes de Layout

-   `div` - Containers
-   `span` - Elementos inline
-   `form` - Formulários
-   `h1` a `h6` - Títulos
-   `p` - Parágrafos

### Componentes de Mídia

-   `img` - Imagens
-   `a` - Links

## 🔧 Configuração

### Opções do ComponentRenderer

```javascript
const options = {
    enableAnimations: true, // Habilitar animações
    enableValidation: true, // Habilitar validação
    debugMode: false, // Modo de debug
};
```

### Opções de Validação

```javascript
const validationOptions = {
    realTimeValidation: true, // Validação em tempo real
    showErrorMessages: true, // Mostrar mensagens de erro
    validateOnSubmit: true, // Validar ao enviar
};
```

## 🎯 Exemplos Práticos

### Exemplo 1: Formulário de Cadastro

```javascript
const formData = {
    page: {
        title: "Cadastro",
        components: [
            {
                type: "h1",
                content: "Cadastro de Usuário",
                attributes: { className: "text-center mb-8" },
            },
            {
                type: "form",
                attributes: { method: "post", action: "/submit" },
                components: [
                    {
                        type: "fieldset",
                        legend: "Dados Pessoais",
                        components: [
                            {
                                type: "div",
                                components: [
                                    {
                                        type: "label",
                                        content: "Nome:",
                                        attributes: { htmlFor: "name" },
                                    },
                                    {
                                        type: "input",
                                        attributes: {
                                            id: "name",
                                            name: "name",
                                            type: "text",
                                            required: true,
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

renderComponentsWithValidation(formData, "#container");
```

### Exemplo 2: Lista de Usuários

```javascript
const userList = {
    type: "div",
    attributes: { className: "space-y-4" },
    components: users.map((user) => ({
        type: "div",
        attributes: { className: "bg-white p-4 rounded shadow" },
        components: [
            {
                type: "h3",
                content: user.name,
                attributes: { className: "text-lg font-semibold" },
            },
            {
                type: "p",
                content: user.email,
                attributes: { className: "text-gray-600" },
            },
            {
                type: "a",
                content: "Ver perfil",
                attributes: {
                    href: `#user/${user.id}`,
                    className: "text-blue-600 hover:underline",
                },
            },
        ],
    })),
};
```

## 🚀 Funcionalidades Avançadas

### Validação Customizada

```javascript
// Adicionar validador de CPF
renderer.addValidator("cpf", function (value) {
    // Implementação da validação de CPF
    return validarCPF(value);
});

// Usar validador
renderer.validateElement($input, { cpf: true });
```

### Animações Customizadas

```javascript
// Adicionar animação personalizada
renderer.addAnimation("zoomIn", function ($element) {
    $element
        .css({
            transform: "scale(0)",
            opacity: 0,
        })
        .animate(
            {
                transform: "scale(1)",
                opacity: 1,
            },
            300
        );
});
```

### Callbacks de Eventos

```javascript
// Configurar callbacks globais
window.onFormValid = function ($form) {
    const data = getFormData($form);
    // Processar dados do formulário
    console.log("Formulário válido:", data);
};

window.onFormError = function ($form, errors) {
    // Tratar erros de validação
    console.error("Erros no formulário:", errors);
};
```

## 📱 Responsividade

O ComponentRenderer v2.0 é totalmente responsivo e funciona perfeitamente em:

-   ✅ Desktop
-   ✅ Tablet
-   ✅ Mobile
-   ✅ PWA (Progressive Web Apps)

## 🔒 Segurança

-   **Validação de entrada**: Todos os inputs são validados
-   **Sanitização**: Conteúdo HTML é sanitizado automaticamente
-   **XSS Protection**: Proteção contra ataques XSS
-   **CSRF Protection**: Suporte a tokens CSRF

## 🎨 Personalização

### CSS Customizado

```css
/* Personalizar estilos de validação */
.validation-error {
    color: #dc2626;
    font-size: 0.875rem;
    margin-top: 0.25rem;
}

/* Personalizar animações */
.animate-fade-in {
    animation: fadeIn 0.6s ease-in-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
```

### Temas

```javascript
// Aplicar tema escuro
const darkTheme = {
    backgroundColor: "#1f2937",
    textColor: "#f9fafb",
    borderColor: "#374151",
};

renderer.applyTheme(darkTheme);
```

## 🧪 Testes

O ComponentRenderer v2.0 inclui suporte para testes:

```javascript
// Teste básico
function testarValidacao() {
    const renderer = new ComponentRenderer();
    const emailValidator = renderer.validators.get("email");

    console.assert(emailValidator("test@example.com") === true);
    console.assert(emailValidator("invalid-email") === false);
}
```

## 📊 Performance

-   **Renderização otimizada**: Renderização eficiente de componentes
-   **Lazy loading**: Carregamento sob demanda de componentes
-   **Debouncing**: Validação com debounce para melhor performance
-   **Memory management**: Gerenciamento eficiente de memória

## 🔄 Migração da v1.0

A migração da v1.0 para v2.0 é simples:

```javascript
// v1.0
renderComponents(jsonData, "#container");

// v2.0 (compatível)
renderComponents(jsonData, "#container");

// v2.0 (com novas funcionalidades)
renderComponentsWithValidation(jsonData, "#container", {
    realTimeValidation: true,
    enableAnimations: true,
});
```

## 📞 Suporte

Para dúvidas, sugestões ou problemas:

1. Verifique a documentação
2. Consulte os exemplos em `example_usage.js`
3. Abra uma issue no repositório
4. Entre em contato com a equipe de desenvolvimento

---

**ComponentRenderer v2.0** - Construindo interfaces web de forma simples e poderosa! 🚀

