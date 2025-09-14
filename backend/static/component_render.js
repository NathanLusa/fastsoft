/**
 * Renderizador de Componentes HTML com jQuery
 * Converte JSON de componentes Python em elementos HTML
 * Versão 2.0 - Suporte completo aos novos componentes
 */

class ComponentRenderer {
    constructor(options = {}) {
        this.eventHandlers = {};
        this.options = {
            enableAnimations: true,
            enableValidation: true,
            debugMode: false,
            ...options,
        };
        this.validators = new Map();
        this.animations = new Map();

        this._initializeDefaultValidators();
        this._initializeDefaultAnimations();
    }

    /**
     * Inicializa validadores padrão
     * @private
     */
    _initializeDefaultValidators() {
        this.validators.set("required", (value) => {
            return value !== null && value !== undefined && value.toString().trim() !== "";
        });

        this.validators.set("email", (value) => {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(value);
        });

        this.validators.set("minLength", (value, min) => {
            return value.length >= min;
        });

        this.validators.set("maxLength", (value, max) => {
            return value.length <= max;
        });

        this.validators.set("pattern", (value, pattern) => {
            const regex = new RegExp(pattern);
            return regex.test(value);
        });
    }

    /**
     * Inicializa animações padrão
     * @private
     */
    _initializeDefaultAnimations() {
        this.animations.set("fadeIn", ($element) => {
            $element.hide().fadeIn(300);
        });

        this.animations.set("slideDown", ($element) => {
            $element.hide().slideDown(300);
        });

        this.animations.set("bounce", ($element) => {
            $element.addClass("animate-bounce");
            setTimeout(() => $element.removeClass("animate-bounce"), 1000);
        });
    }

    /**
     * Aplica animação a um elemento
     * @param {jQuery} $element - Elemento jQuery
     * @param {Object} component - Componente com configurações
     * @private
     */
    _applyAnimation($element, component) {
        const animation = component.animation || "fadeIn";
        const animator = this.animations.get(animation);
        if (animator) {
            animator($element);
        }
    }

    /**
     * Valida um elemento de formulário
     * @param {jQuery} $element - Elemento jQuery
     * @param {Object} rules - Regras de validação
     * @returns {boolean} Se o elemento é válido
     */
    validateElement($element, rules = {}) {
        const value = $element.val();
        let isValid = true;
        const errors = [];

        for (const [rule, ruleValue] of Object.entries(rules)) {
            const validator = this.validators.get(rule);
            if (validator) {
                const result = validator(value, ruleValue);
                if (!result) {
                    isValid = false;
                    errors.push(`${rule}: ${ruleValue}`);
                }
            }
        }

        if (!isValid) {
            this._showValidationError($element, errors);
        } else {
            this._clearValidationError($element);
        }

        return isValid;
    }

    /**
     * Mostra erro de validação
     * @param {jQuery} $element - Elemento jQuery
     * @param {Array} errors - Lista de erros
     * @private
     */
    _showValidationError($element, errors) {
        $element.addClass("border-red-500");
        const $errorDiv = $element.siblings(".validation-error");
        if ($errorDiv.length === 0) {
            const $error = $(`<div class="validation-error text-red-600 text-sm mt-1"></div>`);
            $element.after($error);
            $error.text(errors.join(", "));
        } else {
            $errorDiv.text(errors.join(", "));
        }
    }

    /**
     * Remove erro de validação
     * @param {jQuery} $element - Elemento jQuery
     * @private
     */
    _clearValidationError($element) {
        $element.removeClass("border-red-500");
        $element.siblings(".validation-error").remove();
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

        const componentRenderers = {
            input: () => this.renderInput(component),
            select: () => this.renderSelect(component),
            textarea: () => this.renderTextarea(component),
            button: () => this.renderButton(component),
            label: () => this.renderLabel(component),
            div: () => this.renderDiv(component),
            span: () => this.renderSpan(component),
            form: () => this.renderForm(component),
            checkbox: () => this.renderCheckbox(component),
            radio: () => this.renderRadio(component),
            fieldset: () => this.renderFieldset(component),
            legend: () => this.renderLegend(component),
            img: () => this.renderImage(component),
            a: () => this.renderLink(component),
            h1: () => this.renderHeading(component),
            h2: () => this.renderHeading(component),
            h3: () => this.renderHeading(component),
            h4: () => this.renderHeading(component),
            h5: () => this.renderHeading(component),
            h6: () => this.renderHeading(component),
            p: () => this.renderParagraph(component),
        };

        const renderer = componentRenderers[component.type];
        if (renderer) {
            const $element = renderer();
            if ($element && this.options.enableAnimations) {
                this._applyAnimation($element, component);
            }
            return $element;
        } else {
            if (this.options.debugMode) {
                console.warn("Tipo de componente não suportado:", component.type);
            }
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

    /**
     * Renderiza um fieldset
     */
    renderFieldset(component) {
        const $fieldset = $("<fieldset>");
        const attrs = component.attributes || {};

        // Atributos específicos do fieldset
        if (attrs.disabled) $fieldset.prop("disabled", attrs.disabled);
        if (attrs.form) $fieldset.attr("form", attrs.form);

        // Legend se fornecido
        if (component.legend) {
            const $legend = $("<legend>").text(component.legend);
            this.applyBaseAttributes($legend, {});
            $fieldset.append($legend);
        }

        // Componentes filhos
        if (component.components && Array.isArray(component.components)) {
            component.components.forEach((child) => {
                const $childElement = this.renderComponent(child);
                if ($childElement) {
                    $fieldset.append($childElement);
                }
            });
        }

        this.applyBaseAttributes($fieldset, attrs);
        return $fieldset;
    }

    /**
     * Renderiza uma legend
     */
    renderLegend(component) {
        const $legend = $("<legend>");
        const attrs = component.attributes || {};

        // Conteúdo
        $legend.text(component.content || "");

        this.applyBaseAttributes($legend, attrs);
        return $legend;
    }

    /**
     * Renderiza uma imagem
     */
    renderImage(component) {
        const $img = $("<img>");
        const attrs = component.attributes || {};

        // Atributos específicos da imagem
        if (attrs.src) $img.attr("src", attrs.src);
        if (attrs.alt) $img.attr("alt", attrs.alt);
        if (attrs.width !== undefined) $img.attr("width", attrs.width);
        if (attrs.height !== undefined) $img.attr("height", attrs.height);
        if (attrs.loading) $img.attr("loading", attrs.loading);
        if (attrs.crossOrigin) $img.attr("crossorigin", attrs.crossOrigin);
        if (attrs.useMap) $img.attr("usemap", attrs.useMap);
        if (attrs.isMap) $img.attr("ismap", attrs.isMap);
        if (attrs.decoding) $img.attr("decoding", attrs.decoding);
        if (attrs.fetchPriority) $img.attr("fetchpriority", attrs.fetchPriority);

        // Eventos específicos
        if (attrs.onLoad) {
            $img.on("load", new Function("event", attrs.onLoad));
        }
        if (attrs.onError) {
            $img.on("error", new Function("event", attrs.onError));
        }

        this.applyBaseAttributes($img, attrs);
        return $img;
    }

    /**
     * Renderiza um link
     */
    renderLink(component) {
        const $link = $("<a>");
        const attrs = component.attributes || {};

        // Atributos específicos do link
        if (attrs.href) $link.attr("href", attrs.href);
        if (attrs.target) $link.attr("target", attrs.target);
        if (attrs.rel) $link.attr("rel", attrs.rel);
        if (attrs.download) $link.attr("download", attrs.download);
        if (attrs.hreflang) $link.attr("hreflang", attrs.hreflang);
        if (attrs.type) $link.attr("type", attrs.type);

        // Conteúdo
        $link.html(component.content || "");

        this.applyBaseAttributes($link, attrs);
        return $link;
    }

    /**
     * Renderiza um heading (h1-h6)
     */
    renderHeading(component) {
        const tag = component.type; // h1, h2, h3, etc.
        const $heading = $(`<${tag}>`);
        const attrs = component.attributes || {};

        // Conteúdo
        $heading.html(component.content || "");

        this.applyBaseAttributes($heading, attrs);
        return $heading;
    }

    /**
     * Renderiza um parágrafo
     */
    renderParagraph(component) {
        const $paragraph = $("<p>");
        const attrs = component.attributes || {};

        // Conteúdo
        $paragraph.html(component.content || "");

        this.applyBaseAttributes($paragraph, attrs);
        return $paragraph;
    }

    /**
     * Adiciona um validador customizado
     * @param {string} name - Nome do validador
     * @param {Function} validator - Função de validação
     */
    addValidator(name, validator) {
        this.validators.set(name, validator);
    }

    /**
     * Adiciona uma animação customizada
     * @param {string} name - Nome da animação
     * @param {Function} animation - Função de animação
     */
    addAnimation(name, animation) {
        this.animations.set(name, animation);
    }

    /**
     * Valida um formulário completo
     * @param {string} formSelector - Seletor do formulário
     * @returns {boolean} Se o formulário é válido
     */
    validateForm(formSelector) {
        const $form = $(formSelector);
        let isValid = true;

        $form.find("input, select, textarea").each((index, element) => {
            const $element = $(element);
            const rules = this._extractValidationRules($element);

            if (Object.keys(rules).length > 0) {
                const elementValid = this.validateElement($element, rules);
                if (!elementValid) {
                    isValid = false;
                }
            }
        });

        return isValid;
    }

    /**
     * Extrai regras de validação de um elemento
     * @param {jQuery} $element - Elemento jQuery
     * @returns {Object} Regras de validação
     * @private
     */
    _extractValidationRules($element) {
        const rules = {};

        if ($element.prop("required")) {
            rules.required = true;
        }

        if ($element.attr("type") === "email") {
            rules.email = true;
        }

        const minLength = $element.attr("minlength");
        if (minLength) {
            rules.minLength = parseInt(minLength);
        }

        const maxLength = $element.attr("maxlength");
        if (maxLength) {
            rules.maxLength = parseInt(maxLength);
        }

        const pattern = $element.attr("pattern");
        if (pattern) {
            rules.pattern = pattern;
        }

        return rules;
    }
}

// Função utilitária para uso global
window.ComponentRenderer = ComponentRenderer;

// Instância global do renderer com configurações padrão
window.componentRenderer = new ComponentRenderer({
    enableAnimations: true,
    enableValidation: true,
    debugMode: false,
});

// Função de conveniência para renderizar diretamente
function renderComponents(jsonData, targetSelector = "body", options = {}) {
    const renderer = options.renderer || new ComponentRenderer(options);
    renderer.renderPage(jsonData, targetSelector);
    return renderer;
}

// Função para renderizar com validação
function renderComponentsWithValidation(jsonData, targetSelector = "body", validationOptions = {}) {
    const renderer = new ComponentRenderer({
        enableValidation: true,
        ...validationOptions,
    });

    renderer.renderPage(jsonData, targetSelector);

    // Adiciona validação em tempo real
    if (validationOptions.realTimeValidation) {
        $(targetSelector)
            .find("input, select, textarea")
            .on("blur", function () {
                const $element = $(this);
                const rules = renderer._extractValidationRules($element);
                if (Object.keys(rules).length > 0) {
                    renderer.validateElement($element, rules);
                }
            });
    }

    return renderer;
}

// Exemplo de uso com AJAX
function loadAndRenderForm(url, targetSelector = "#form-container", options = {}) {
    const $target = $(targetSelector);

    // Mostra loading
    if (options.showLoading !== false) {
        $target.html(
            '<div class="flex justify-center items-center p-8"><div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div></div>'
        );
    }

    $.ajax({
        url: url,
        method: "GET",
        dataType: "json",
        timeout: options.timeout || 10000,
        success: function (data) {
            const renderer = renderComponents(data, targetSelector, options);

            // Adiciona validação se habilitada
            if (options.enableValidation) {
                $(targetSelector)
                    .find("form")
                    .on("submit", function (e) {
                        e.preventDefault();
                        const isValid = renderer.validateForm(this);
                        if (isValid) {
                            if (options.onValidSubmit) {
                                options.onValidSubmit($(this));
                            } else {
                                this.submit();
                            }
                        }
                    });
            }
        },
        error: function (xhr, status, error) {
            console.error("Erro ao carregar formulário:", error);
            const errorMessage = options.errorMessage || "Erro ao carregar formulário";
            $target.html(
                `<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">${errorMessage}</div>`
            );

            if (options.onError) {
                options.onError(xhr, status, error);
            }
        },
    });
}

// Função melhorada para carregar da API
async function loadFromAPI(options = {}) {
    const url = $("#apiUrl").val().trim();
    if (!url) {
        showError("Por favor, insira uma URL válida");
        return;
    }

    showLoading();

    try {
        const response = await $.ajax({
            url: url,
            method: "GET",
            dataType: "json",
            timeout: options.timeout || 10000,
        });

        const json = typeof response === "string" ? JSON.parse(response) : response;
        hideLoading();
        renderPage(json, options);
    } catch (error) {
        hideLoading();
        showError(`Erro ao carregar dados: ${error.statusText || error.message}`);
    }
}

// Função melhorada para renderizar página
function renderPage(json, options = {}) {
    const targetSelector = options.targetSelector || "#componentContainer";
    const renderer = new ComponentRenderer({
        enableAnimations: options.enableAnimations !== false,
        enableValidation: options.enableValidation !== false,
        debugMode: options.debugMode || false,
    });

    renderer.renderPage(json, targetSelector);

    // Adiciona funcionalidades extras se habilitadas
    if (options.enableValidation) {
        addFormValidation(targetSelector);
    }

    if (options.enableAnimations) {
        addScrollAnimations(targetSelector);
    }

    return renderer;
}

// Função para adicionar validação de formulário
function addFormValidation(containerSelector) {
    $(containerSelector)
        .find("form")
        .each(function () {
            const $form = $(this);

            $form.on("submit", function (e) {
                e.preventDefault();
                const isValid = window.componentRenderer.validateForm(this);

                if (isValid) {
                    // Formulário válido - pode enviar
                    if (window.onFormValid) {
                        window.onFormValid($form);
                    } else {
                        // Comportamento padrão: enviar formulário
                        this.submit();
                    }
                } else {
                    // Mostrar mensagem de erro geral
                    showError("Por favor, corrija os erros no formulário");
                }
            });

            // Validação em tempo real
            $form.find("input, select, textarea").on("blur", function () {
                const $element = $(this);
                const rules = window.componentRenderer._extractValidationRules($element);
                if (Object.keys(rules).length > 0) {
                    window.componentRenderer.validateElement($element, rules);
                }
            });
        });
}

// Função para adicionar animações de scroll
function addScrollAnimations(containerSelector) {
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("animate-fade-in");
                }
            });
        },
        { threshold: 0.1 }
    );

    $(containerSelector)
        .find("[data-animate]")
        .each(function () {
            observer.observe(this);
        });
}

// Funções utilitárias para UI
function showLoading(message = "Carregando...") {
    const $container = $("#componentContainer");
    $container.html(`
        <div class="flex flex-col items-center justify-center p-8">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
            <p class="text-gray-600">${message}</p>
        </div>
    `);
}

function hideLoading() {
    // Loading será substituído pelo conteúdo renderizado
}

function showError(message) {
    const $container = $("#componentContainer");
    $container.html(`
        <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            <div class="flex items-center">
                <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                </svg>
                ${message}
            </div>
        </div>
    `);
}

function showSuccess(message) {
    const $container = $("#componentContainer");
    $container.html(`
        <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
            <div class="flex items-center">
                <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
                ${message}
            </div>
        </div>
    `);
}

// Função para obter dados do formulário
function getFormData(formSelector) {
    const $form = $(formSelector);
    const formData = {};

    $form.find("input, select, textarea").each(function () {
        const $element = $(this);
        const name = $element.attr("name");
        const type = $element.attr("type");

        if (name) {
            if (type === "checkbox" || type === "radio") {
                if ($element.is(":checked")) {
                    formData[name] = $element.val();
                }
            } else {
                formData[name] = $element.val();
            }
        }
    });

    return formData;
}

// Função para limpar formulário
function clearForm(formSelector) {
    $(formSelector)
        .find("input, select, textarea")
        .each(function () {
            const $element = $(this);
            const type = $element.attr("type");

            if (type === "checkbox" || type === "radio") {
                $element.prop("checked", false);
            } else {
                $element.val("");
            }

            // Limpar erros de validação
            window.componentRenderer._clearValidationError($element);
        });
}

// Inicialização quando o documento estiver pronto
$(document).ready(function () {
    // Event listeners básicos
    $("#loadComponents").on("click", () => loadFromAPI());

    // Permitir carregar com Enter na URL
    $("#apiUrl").on("keypress", (e) => {
        if (e.which === 13) loadFromAPI();
    });

    // Adicionar CSS para animações
    if (!document.getElementById("component-renderer-styles")) {
        const style = document.createElement("style");
        style.id = "component-renderer-styles";
        style.textContent = `
            .animate-fade-in {
                animation: fadeIn 0.6s ease-in-out;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .validation-error {
                animation: shake 0.5s ease-in-out;
            }
            
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-5px); }
                75% { transform: translateX(5px); }
            }
        `;
        document.head.appendChild(style);
    }
});
