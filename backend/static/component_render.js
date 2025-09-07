/**
 * Renderizador de Componentes HTML com jQuery
 * Converte JSON de componentes Python em elementos HTML
 */

class ComponentRenderer {
    constructor() {
        this.eventHandlers = {};
    }

    /**
     * Renderiza uma página completa
     * @param {Object} pageData - Dados da página
     * @param {string} targetSelector - Seletor do elemento onde renderizar
     */
    renderPage(pageData, targetSelector = "body") {
        const $target = $(targetSelector);
        const $div = $(`<div></div>`);

        $target.empty();

        if (pageData.page) {
            const page = pageData.page;

            // Adiciona título se existir
            if (page.title) {
                document.title = page.title;
                $target.append(`
                    <div class="bg-white rounded-lg shadow-sm border p-6 mb-6">
                        <h2 class="text-2xl font-bold text-gray-800">${page.title}</h2>
                    </div>
                `);
            }

            // Adiciona classe de layout se especificada
            if (page.layout) {
                $div.addClass(this.getLayoutClass(page.layout));
                // $div.addClass(`layout-${page.layout}`);
            }

            // Renderiza componentes
            if (page.components && Array.isArray(page.components)) {
                page.components.forEach((component) => {
                    const $element = this.renderComponent(component);
                    if ($element) {
                        $div.append($element);
                    }
                });
            }
        } else {
            // Se não for uma página, renderiza como componente único
            const $element = this.renderComponent(pageData);
            if ($element) {
                $div.append($element);
            }
        }

        $target.append($div);
    }

    getLayoutClass(layout) {
        switch (layout) {
            case "grid":
                return "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6";
            case "flex":
                return "flex flex-wrap gap-6";
            case "single":
                return "space-y-6";
            default:
                return "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6";
        }
    }

    /**
     * Renderiza um componente individual
     * @param {Object} component - Dados do componente
     * @returns {jQuery} Elemento jQuery
     */
    renderComponent(component) {
        if (!component || !component.type) {
            console.warn("Componente inválido:", component);
            return null;
        }

        switch (component.type) {
            case "input":
                return this.renderInput(component);
            case "select":
                return this.renderSelect(component);
            case "textarea":
                return this.renderTextarea(component);
            case "button":
                return this.renderButton(component);
            case "label":
                return this.renderLabel(component);
            case "div":
                return this.renderDiv(component);
            case "span":
                return this.renderSpan(component);
            case "form":
                return this.renderForm(component);
            case "checkbox":
                return this.renderCheckbox(component);
            case "radio":
                return this.renderRadio(component);
            default:
                console.warn("Tipo de componente não suportado:", component.type);
                return null;
        }
    }

    /**
     * Aplica atributos base a um elemento
     * @param {jQuery} $element - Elemento jQuery
     * @param {Object} attributes - Atributos do componente
     */
    applyBaseAttributes($element, attributes) {
        if (!attributes) return;

        // Atributos básicos
        if (attributes.id) $element.attr("id", attributes.id);
        if (attributes.className) $element.addClass(attributes.className);
        if (attributes.title) $element.attr("title", attributes.title);
        if (attributes.lang) $element.attr("lang", attributes.lang);
        if (attributes.dir) $element.attr("dir", attributes.dir);
        if (attributes.hidden) $element.attr("hidden", attributes.hidden);
        if (attributes.tabIndex !== undefined) $element.attr("tabindex", attributes.tabIndex);
        if (attributes.accessKey) $element.attr("accesskey", attributes.accessKey);
        if (attributes.contentEditable) $element.attr("contenteditable", attributes.contentEditable);
        if (attributes.draggable) $element.attr("draggable", attributes.draggable);
        if (attributes.spellCheck !== undefined) $element.attr("spellcheck", attributes.spellCheck);
        if (attributes.translate !== undefined) $element.attr("translate", attributes.translate ? "yes" : "no");
        if (attributes.role) $element.attr("role", attributes.role);
        if (attributes.ariaLabel) $element.attr("aria-label", attributes.ariaLabel);
        if (attributes.ariaDescribedBy) $element.attr("aria-describedby", attributes.ariaDescribedBy);
        if (attributes.ariaLabelledBy) $element.attr("aria-labelledby", attributes.ariaLabelledBy);

        // Estilos
        if (attributes.style && typeof attributes.style === "object") {
            $element.css(attributes.style);
        }

        // Atributos data-
        if (attributes.dataAttributes) {
            Object.entries(attributes.dataAttributes).forEach(([key, value]) => {
                $element.attr(`data-${key}`, value);
            });
        }

        // Eventos
        this.bindEvents($element, attributes);
    }

    /**
     * Vincula eventos a um elemento
     * @param {jQuery} $element - Elemento jQuery
     * @param {Object} attributes - Atributos com eventos
     */
    bindEvents($element, attributes) {
        const events = [
            "onClick",
            "onFocus",
            "onBlur",
            "onKeyDown",
            "onKeyUp",
            "onKeyPress",
            "onChange",
            "onInput",
            "onSubmit",
            "onReset",
            "onScroll",
        ];

        events.forEach((eventAttr) => {
            if (attributes[eventAttr]) {
                const eventName = eventAttr.replace("on", "").toLowerCase();
                const handler = attributes[eventAttr];

                if (typeof handler === "string") {
                    // Se for string, assume que é código JavaScript
                    $element.on(eventName, new Function("event", handler));
                } else if (typeof handler === "function") {
                    $element.on(eventName, handler);
                }
            }
        });
    }

    /**
     * Renderiza um input
     */
    renderInput(component) {
        const $input = $("<input>");
        const attrs = component.attributes || {};

        // Atributos específicos do input
        if (attrs.type) $input.attr("type", attrs.type);
        if (attrs.value !== undefined) $input.val(attrs.value);
        if (attrs.placeholder) $input.attr("placeholder", attrs.placeholder);
        if (attrs.name) $input.attr("name", attrs.name);
        if (attrs.disabled) $input.prop("disabled", attrs.disabled);
        if (attrs.readonly) $input.prop("readonly", attrs.readonly);
        if (attrs.required) $input.prop("required", attrs.required);
        if (attrs.autofocus) $input.prop("autofocus", attrs.autofocus);
        if (attrs.autocomplete) $input.attr("autocomplete", attrs.autocomplete);
        if (attrs.maxLength !== undefined) $input.attr("maxlength", attrs.maxLength);
        if (attrs.minLength !== undefined) $input.attr("minlength", attrs.minLength);
        if (attrs.max) $input.attr("max", attrs.max);
        if (attrs.min) $input.attr("min", attrs.min);
        if (attrs.step) $input.attr("step", attrs.step);
        if (attrs.pattern) $input.attr("pattern", attrs.pattern);
        if (attrs.size) $input.attr("size", attrs.size);
        if (attrs.multiple) $input.prop("multiple", attrs.multiple);
        if (attrs.accept) $input.attr("accept", attrs.accept);
        if (attrs.capture) $input.attr("capture", attrs.capture);
        if (attrs.list) $input.attr("list", attrs.list);
        if (attrs.checked) $input.prop("checked", attrs.checked);

        this.applyBaseAttributes($input, attrs);
        return $input;
    }

    /**
     * Renderiza um select
     */
    renderSelect(component) {
        const $select = $("<select>");
        const attrs = component.attributes || {};

        // Atributos específicos do select
        if (attrs.name) $select.attr("name", attrs.name);
        if (attrs.disabled) $select.prop("disabled", attrs.disabled);
        if (attrs.required) $select.prop("required", attrs.required);
        if (attrs.autofocus) $select.prop("autofocus", attrs.autofocus);
        if (attrs.multiple) $select.prop("multiple", attrs.multiple);
        if (attrs.size) $select.attr("size", attrs.size);

        // Adiciona opções
        if (component.options && Array.isArray(component.options)) {
            component.options.forEach((option) => {
                const $option = $("<option>");
                const optAttrs = option.attributes || {};

                if (optAttrs.value !== undefined) $option.val(optAttrs.value);
                if (optAttrs.selected) $option.prop("selected", optAttrs.selected);
                if (optAttrs.disabled) $option.prop("disabled", optAttrs.disabled);

                $option.text(option.content || "");
                $select.append($option);
            });
        }

        this.applyBaseAttributes($select, attrs);
        return $select;
    }

    /**
     * Renderiza um textarea
     */
    renderTextarea(component) {
        const $textarea = $("<textarea>");
        const attrs = component.attributes || {};

        // Atributos específicos do textarea
        if (attrs.name) $textarea.attr("name", attrs.name);
        if (attrs.disabled) $textarea.prop("disabled", attrs.disabled);
        if (attrs.readonly) $textarea.prop("readonly", attrs.readonly);
        if (attrs.required) $textarea.prop("required", attrs.required);
        if (attrs.autofocus) $textarea.prop("autofocus", attrs.autofocus);
        if (attrs.placeholder) $textarea.attr("placeholder", attrs.placeholder);
        if (attrs.rows) $textarea.attr("rows", attrs.rows);
        if (attrs.cols) $textarea.attr("cols", attrs.cols);
        if (attrs.maxLength !== undefined) $textarea.attr("maxlength", attrs.maxLength);
        if (attrs.minLength !== undefined) $textarea.attr("minlength", attrs.minLength);
        if (attrs.wrap) $textarea.attr("wrap", attrs.wrap);
        if (attrs.autocomplete) $textarea.attr("autocomplete", attrs.autocomplete);

        // Conteúdo
        if (component.content) $textarea.text(component.content);

        this.applyBaseAttributes($textarea, attrs);
        return $textarea;
    }

    /**
     * Renderiza um button
     */
    renderButton(component) {
        const $button = $("<button>");
        const attrs = component.attributes || {};

        // Atributos específicos do button
        if (attrs.type) $button.attr("type", attrs.type);
        if (attrs.name) $button.attr("name", attrs.name);
        if (attrs.value) $button.attr("value", attrs.value);
        if (attrs.disabled) $button.prop("disabled", attrs.disabled);
        if (attrs.autofocus) $button.prop("autofocus", attrs.autofocus);
        if (attrs.formAction) $button.attr("formaction", attrs.formAction);
        if (attrs.formEncType) $button.attr("formenctype", attrs.formEncType);
        if (attrs.formMethod) $button.attr("formmethod", attrs.formMethod);
        if (attrs.formNoValidate) $button.attr("formnovalidate", attrs.formNoValidate);
        if (attrs.formTarget) $button.attr("formtarget", attrs.formTarget);

        // Conteúdo
        $button.html(component.content || "Button");

        this.applyBaseAttributes($button, attrs);
        return $button;
    }

    /**
     * Renderiza um label
     */
    renderLabel(component) {
        const $label = $("<label>");
        const attrs = component.attributes || {};

        // Atributos específicos do label
        if (attrs.htmlFor) $label.attr("for", attrs.htmlFor);

        // Conteúdo
        $label.html(component.content || "");

        this.applyBaseAttributes($label, attrs);
        return $label;
    }

    /**
     * Renderiza uma div
     */
    renderDiv(component) {
        const $div = $("<div>");
        const attrs = component.attributes || {};

        // Conteúdo texto
        if (component.content) {
            $div.html(component.content);
        }

        // Componentes filhos
        if (component.components && Array.isArray(component.components)) {
            component.components.forEach((child) => {
                const $childElement = this.renderComponent(child);
                if ($childElement) {
                    $div.append($childElement);
                }
            });
        }

        this.applyBaseAttributes($div, attrs);
        return $div;
    }

    /**
     * Renderiza um span
     */
    renderSpan(component) {
        const $span = $("<span>");
        const attrs = component.attributes || {};

        // Conteúdo
        $span.html(component.content || "");

        this.applyBaseAttributes($span, attrs);
        return $span;
    }

    /**
     * Renderiza um form
     */
    renderForm(component) {
        const $form = $("<form>");
        const attrs = component.attributes || {};

        // Atributos específicos do form
        if (attrs.action) $form.attr("action", attrs.action);
        if (attrs.method) $form.attr("method", attrs.method);
        if (attrs.encType) $form.attr("enctype", attrs.encType);
        if (attrs.target) $form.attr("target", attrs.target);
        if (attrs.acceptCharset) $form.attr("accept-charset", attrs.acceptCharset);
        if (attrs.autocomplete) $form.attr("autocomplete", attrs.autocomplete);
        if (attrs.noValidate) $form.attr("novalidate", attrs.noValidate);

        // Componentes filhos
        if (component.components && Array.isArray(component.components)) {
            component.components.forEach((child) => {
                const $childElement = this.renderComponent(child);
                if ($childElement) {
                    $form.append($childElement);
                }
            });
        }

        this.applyBaseAttributes($form, attrs);
        return $form;
    }

    /**
     * Renderiza um checkbox
     */
    renderCheckbox(component) {
        const $wrapper = $('<div class="checkbox-wrapper flex items-center space-x-2">');
        const $input = $('<input type="checkbox">');
        const attrs = component.attributes || {};

        // Atributos específicos do checkbox
        if (attrs.name) $input.attr("name", attrs.name);
        if (attrs.value) $input.attr("value", attrs.value);
        if (attrs.checked) $input.prop("checked", attrs.checked);
        if (attrs.disabled) $input.prop("disabled", attrs.disabled);
        if (attrs.required) $input.prop("required", attrs.required);
        if (attrs.autofocus) $input.prop("autofocus", attrs.autofocus);

        this.applyBaseAttributes($input, attrs);
        $wrapper.append($input);

        // Label se fornecido
        if (component.label) {
            const $label = $("<label>");
            if (attrs.id) $label.attr("for", attrs.id);
            $label.text(component.label);
            $wrapper.append($label);
        }

        return $wrapper;
    }

    /**
     * Renderiza um radio button
     */
    renderRadio(component) {
        const $wrapper = $('<div class="radio-wrapper">');
        const $input = $('<input type="radio">');
        const attrs = component.attributes || {};

        // Atributos específicos do radio
        if (attrs.name) $input.attr("name", attrs.name);
        if (attrs.value) $input.attr("value", attrs.value);
        if (attrs.checked) $input.prop("checked", attrs.checked);
        if (attrs.disabled) $input.prop("disabled", attrs.disabled);
        if (attrs.required) $input.prop("required", attrs.required);
        if (attrs.autofocus) $input.prop("autofocus", attrs.autofocus);

        this.applyBaseAttributes($input, attrs);
        $wrapper.append($input);

        // Label se fornecido
        if (component.label) {
            const $label = $("<label>");
            if (attrs.id) $label.attr("for", attrs.id);
            $label.text(component.label);
            $wrapper.append($label);
        }

        return $wrapper;
    }
}

// Função utilitária para uso global
window.ComponentRenderer = ComponentRenderer;

// Função de conveniência para renderizar diretamente
function renderComponents(jsonData, targetSelector = "body") {
    const renderer = new ComponentRenderer();
    renderer.renderPage(jsonData, targetSelector);
}

// Exemplo de uso com AJAX
function loadAndRenderForm(url, targetSelector = "#form-container") {
    $.ajax({
        url: url,
        method: "GET",
        dataType: "json",
        success: function (data) {
            renderComponents(data, targetSelector);
        },
        error: function (xhr, status, error) {
            console.error("Erro ao carregar formulário:", error);
            $(targetSelector).html('<div class="error">Erro ao carregar formulário</div>');
        },
    });
}

async function loadFromAPI() {
    const url = $("#apiUrl").val().trim();
    if (!url) {
        // this.showError("Por favor, insira uma URL válida");
        return;
    }

    // this.showLoading();

    // try {
    const response = await $.ajax({
        url: url,
        method: "GET",
        dataType: "json",
        timeout: 10000,
    });

    const json = JSON.parse(response);

    // this.hideLoading();
    renderPage(json);
    // } catch (error) {
    //     this.showError(`Erro ao carregar dados: ${error.statusText || error.message}`);
    // }
}

function renderPage(json) {
    // Renderizar JSON diretamente
    const renderer = new ComponentRenderer();
    renderer.renderPage(json, "#componentContainer");

    // Ou usar a função utilitária
    // renderComponents(jsonFromPython, "#componentContainer");

    // Carregar via AJAX
    // loadAndRenderForm("/api/form-endpoint", "#form-container");
}

$(document).ready(function () {
    $("#loadComponents").on("click", () => loadFromAPI());

    // Permitir carregar com Enter na URL
    $("#apiUrl").on("keypress", (e) => {
        if (e.which === 13) loadFromAPI();
    });
});
