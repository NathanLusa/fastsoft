class ComponentRenderer {
    constructor() {
        this.container = $("#componentContainer");
        this.setupEventHandlers();
    }

    setupEventHandlers() {
        $("#loadComponents").on("click", () => this.loadFromAPI());
        $("#loadExample").on("click", () => this.loadExample());

        // Permitir carregar com Enter na URL
        $("#apiUrl").on("keypress", (e) => {
            if (e.which === 13) this.loadFromAPI();
        });
    }

    showLoading() {
        $("#loading").removeClass("hidden");
        $("#error").addClass("hidden");
    }

    hideLoading() {
        $("#loading").addClass("hidden");
    }

    showError(message) {
        $("#errorMessage").text(message);
        $("#error").removeClass("hidden");
        this.hideLoading();
    }

    async loadFromAPI() {
        const url = $("#apiUrl").val().trim();
        if (!url) {
            this.showError("Por favor, insira uma URL válida");
            return;
        }

        this.showLoading();

        // try {
        const response = await $.ajax({
            url: url,
            method: "GET",
            dataType: "json",
            timeout: 10000,
        });

        const json = JSON.parse(response);

        this.hideLoading();
        this.renderPage(json);
        // } catch (error) {
        //     this.showError(`Erro ao carregar dados: ${error.statusText || error.message}`);
        // }
    }

    loadExample() {
        // Exemplo de JSON que pode vir do backend
        const exampleData = {
            page: {
                title: "Dashboard Principal",
                layout: "grid",
                components: [
                    {
                        type: "card",
                        id: "card-1",
                        attributes: {
                            title: "Vendas Totais",
                            value: "R$ 125.430",
                            icon: "💰",
                            color: "blue",
                            trend: "+12%",
                        },
                    },
                    {
                        type: "chart",
                        id: "chart-1",
                        attributes: {
                            title: "Vendas por Mês",
                            type: "line",
                            data: [
                                { month: "Jan", value: 4000 },
                                { month: "Fev", value: 3000 },
                                { month: "Mar", value: 5000 },
                                { month: "Abr", value: 4500 },
                                { month: "Mai", value: 6000 },
                                { month: "Jun", value: 5500 },
                            ],
                        },
                    },
                    {
                        type: "list",
                        id: "list-1",
                        attributes: {
                            title: "Últimas Transações",
                            items: [
                                { id: 1, name: "Produto A", value: "R$ 299", status: "completed" },
                                { id: 2, name: "Produto B", value: "R$ 150", status: "pending" },
                                { id: 3, name: "Produto C", value: "R$ 75", status: "completed" },
                                { id: 4, name: "Produto D", value: "R$ 420", status: "failed" },
                            ],
                        },
                    },
                    {
                        type: "form",
                        id: "form-1",
                        attributes: {
                            title: "Adicionar Produto",
                            fields: [
                                { name: "name", label: "Nome", type: "text", required: true },
                                { name: "price", label: "Preço", type: "number", required: true },
                                {
                                    name: "category",
                                    label: "Categoria",
                                    type: "select",
                                    options: ["Eletrônicos", "Roupas", "Casa"],
                                },
                                { name: "description", label: "Descrição", type: "textarea", required: false },
                            ],
                        },
                    },
                ],
            },
        };

        this.renderComponents(exampleData);
    }

    renderPage(data) {
        this.container.empty();

        console.log(data);
        console.log(data.page);
        console.log(data.page.components);
        if (!data.page || !data.page.components) {
            this.showError("Estrutura de dados inválida");
            return;
        }

        // Renderizar título da página se existir
        if (data.page.title) {
            this.container.append(`
                <div class="bg-white rounded-lg shadow-sm border p-6 mb-6">
                    <h2 class="text-2xl font-bold text-gray-800">${data.page.title}</h2>
                </div>
            `);
        }

        // Determinar layout
        const layoutClass = this.getLayoutClass(data.page.layout);
        // const componentsWrapper = $(`<div class="${layoutClass}"></div>`);

        // Renderizar cada componente
        // data.page.components.forEach((component) => {
        //     const renderedComponent = this.renderComponent(component);
        //     if (renderedComponent) {
        //         componentsWrapper.append(renderedComponent);
        //     }
        // });

        const c = this.renderComponents(data.page.components, layoutClass);
        console.log("teste: ", c);
        this.container.append(c);
    }

    renderComponents(components, layoutClass) {
        // Determinar layout
        // const layoutClass = this.getLayoutClass(data.page.layout);
        const componentsWrapper = $(`<div class="${layoutClass}"></div>`);
        // const componentsWrapper = $(`<div class=""></div>`);
        // const componentsWrapper = "";

        // Renderizar cada componente
        components.forEach((component) => {
            const renderedComponent = this.renderComponent(component);
            if (renderedComponent) {
                componentsWrapper.append(renderedComponent);
            }
        });

        // this.container.append(componentsWrapper);
        return componentsWrapper;
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

    renderComponent(component) {
        console.log("renderComponent");
        console.log(component);
        switch (component.type) {
            case "card":
                return this.renderCard(component);
            case "chart":
                return this.renderChart(component);
            case "list":
                return this.renderList(component);
            case "form":
                return this.renderForm(component);
            case "button":
                return this.renderButton(component);
            case "text":
                return this.renderText(component);
            case "select":
                return this.renderSelect(component);
            case "textarea":
                return this.renderTextArea(component);
            case "input":
                return this.renderInput(component);
            case "label":
                return this.renderLabel(component);
            case "div":
                return this.renderDiv(component);
            default:
                return this.renderGeneric(component);
        }
        // return ReadableByteStreamController;
    }

    renderCard(component) {
        const { title, value, icon, color, trend } = component.attributes;
        const colorClasses = this.getColorClasses(color);

        return $(`
            <div class="component-container bg-white rounded-lg shadow-sm border p-6" data-id="${component.id}">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm font-medium text-gray-600">${title}</p>
                        <p class="text-2xl font-bold ${colorClasses.text}">${value}</p>
                        ${trend ? `<p class="text-sm text-green-600 mt-1">${trend}</p>` : ""}
                    </div>
                    <div class="text-3xl">${icon || "📊"}</div>
                </div>
            </div>
        `);
    }

    renderChart(component) {
        const { title, data, type } = component.attributes;

        const chartElement = $(`
            <div class="component-container bg-white rounded-lg shadow-sm border p-6 col-span-2" data-id="${component.id}">
                <h3 class="text-lg font-semibold mb-4">${title}</h3>
                <div class="chart-container">
                    <canvas id="chart-${component.id}" width="400" height="200"></canvas>
                </div>
            </div>
        `);

        // Simular gráfico com barras CSS (em um projeto real usaria Chart.js)
        const maxValue = Math.max(...data.map((d) => d.value));
        const chartBars = data
            .map(
                (d) => `
            <div class="flex items-end justify-center text-sm">
                <div class="bg-blue-500 rounded-t" style="height: ${(d.value / maxValue) * 150}px; width: 30px;"></div>
            </div>
            <div class="text-center text-xs text-gray-600 mt-2">${d.month}</div>
        `
            )
            .join("");

        chartElement.find(".chart-container").html(`
            <div class="flex items-end justify-around space-x-2 h-40">
                ${data
                    .map(
                        (d) => `
                    <div class="flex flex-col items-center">
                        <div class="bg-blue-500 rounded-t mb-2" style="height: ${
                            (d.value / maxValue) * 120
                        }px; width: 40px;"></div>
                        <span class="text-xs text-gray-600">${d.month}</span>
                        <span class="text-xs font-medium">${d.value}</span>
                    </div>
                `
                    )
                    .join("")}
            </div>
        `);

        return chartElement;
    }

    renderDiv(component) {
        const componentsWrapper = $(`<div ${JSON.stringify(component.attributes, null, 2)}></div>`);

        if (component.components != null) {
            component.components.forEach((component) => {
                const renderedComponent = this.renderComponent(component);
                if (renderedComponent) {
                    componentsWrapper.append(renderedComponent);
                }
            });
        }

        return componentsWrapper;
    }

    renderList(component) {
        const { title, items } = component.attributes;

        const listItems = items
            .map((item) => {
                const statusColor = this.getStatusColor(item.status);
                return `
                <div class="flex items-center justify-between py-3 border-b border-gray-100 last:border-b-0">
                    <div>
                        <p class="font-medium text-gray-800">${item.name}</p>
                        <p class="text-sm text-gray-600">${item.value}</p>
                    </div>
                    <span class="px-2 py-1 text-xs font-medium rounded-full ${statusColor}">
                        ${item.status}
                    </span>
                </div>
            `;
            })
            .join("");

        return $(`
            <div class="component-container bg-white rounded-lg shadow-sm border p-6" data-id="${component.id}">
                <h3 class="text-lg font-semibold mb-4">${title}</h3>
                <div class="space-y-0">
                    ${listItems}
                </div>
            </div>
        `);
    }

    renderSelect(component) {
        const options = component.options.map((opt) => `<option value="${opt}">${opt}</option>`).join("");
        return `
        <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">${component.label}</label>
            <select name="${component.name}" class="w-full border border-gray-300 rounded-lg px-3 py-2" ${
            component.required ? "required" : ""
        }>
                <option value="">Selecione...</option>
                ${options}
            </select>
        </div>`;
    }

    renderTextArea(component) {
        return `
        <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">${component.label}</label>
            <textarea name="${component.name}" class="w-full border border-gray-300 rounded-lg px-3 py-2" rows="3" ${
            component.required ? "required" : ""
        }></textarea>
        </div>`;
    }

    renderInput(component) {
        return `<input ${JSON.stringify(component.attributes, null, 2)}>`;
    }

    renderForm(component) {
        const { title } = component.attributes;

        const formComponents = component.components
            .map((item) => {
                const c = this.renderComponent(item);
                console.log("component form: ", c.text());
                return c.text();
            })
            .join("");
        // const formComponents = component.components.map((item) => this.renderComponent(item));
        console.log("Componentes do form: ", formComponents);

        return $(`
            <div class="component-container bg-white rounded-lg shadow-sm border p-6" data-id="${component.id}">
                <h3 class="text-lg font-semibold mb-4">${title}</h3>
                <form class="space-y-4">
                    ${formComponents}
                    <button type="submit" class="w-full bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded-lg transition-colors">
                        Salvar
                    </button>
                </form>
            </div>
        `);
    }

    renderButton(component) {
        const { text, color, size, action } = component.attributes;
        const colorClasses = this.getColorClasses(color);
        const sizeClass = size === "large" ? "px-6 py-3 text-lg" : "px-4 py-2";

        return $(`
            <div class="component-container" data-id="${component.id}">
                <button class="${colorClasses.bg} ${colorClasses.hover} text-white font-medium ${sizeClass} rounded-lg transition-colors" 
                        onclick="handleAction('${action}', '${component.id}')">
                    ${text}
                </button>
            </div>
        `);
    }

    renderText(component) {
        const { content, size, color } = component.attributes;
        const sizeClass = this.getTextSize(size);
        const colorClass = color ? `text-${color}-600` : "text-gray-800";

        return $(`
            <div class="component-container" data-id="${component.id}">
                <p class="${sizeClass} ${colorClass}">${content}</p>
            </div>
        `);
    }

    renderGeneric(component) {
        return $(`
            <div class="component-container bg-gray-100 rounded-lg p-4 border-2 border-dashed border-gray-300" data-id="${
                component.id
            }">
                <p class="text-gray-600 text-center">
                    <strong>Componente desconhecido:</strong> ${component.type}
                </p>
                <pre class="text-xs mt-2 text-gray-500">${JSON.stringify(component.attributes, null, 2)}</pre>
            </div>
        `);
    }

    renderLabel(component) {
        return `<label class="${component.class}" htmlFor="${component.html_for}" ${JSON.stringify(
            component.attributes,
            null,
            2
        )}>${component.content}</label>`;
    }

    getColorClasses(color) {
        const colors = {
            blue: { bg: "bg-blue-500", hover: "hover:bg-blue-600", text: "text-blue-600" },
            green: { bg: "bg-green-500", hover: "hover:bg-green-600", text: "text-green-600" },
            red: { bg: "bg-red-500", hover: "hover:bg-red-600", text: "text-red-600" },
            yellow: { bg: "bg-yellow-500", hover: "hover:bg-yellow-600", text: "text-yellow-600" },
            purple: { bg: "bg-purple-500", hover: "hover:bg-purple-600", text: "text-purple-600" },
        };
        return colors[color] || colors.blue;
    }

    getStatusColor(status) {
        const colors = {
            completed: "bg-green-100 text-green-800",
            pending: "bg-yellow-100 text-yellow-800",
            failed: "bg-red-100 text-red-800",
        };
        return colors[status] || "bg-gray-100 text-gray-800";
    }

    getTextSize(size) {
        const sizes = {
            small: "text-sm",
            medium: "text-base",
            large: "text-lg",
            xl: "text-xl",
            "2xl": "text-2xl",
        };
        return sizes[size] || "text-base";
    }
}

// Função global para lidar com ações de botões
function handleAction(action, componentId) {
    console.log(`Ação '${action}' executada no componente '${componentId}'`);
    alert(`Ação executada: ${action}`);
}

// Inicializar quando o documento estiver pronto
$(document).ready(function () {
    const renderer = new ComponentRenderer();

    // Carregar exemplo automaticamente
    // renderer.loadExample();
});
