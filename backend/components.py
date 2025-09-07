import json
from typing import Dict, List, Any, Optional, Union
from abc import ABC, abstractmethod


class StyleProvider:
    """Provedor de estilos padrão usando Tailwind CSS"""
    
    DEFAULT_STYLES = {
        'button': {
            'class_name': 'px-4 py-2 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200',
            'style': {}
        },
        'button_danger': {
            'class_name': 'px-4 py-2 bg-red-600 text-white font-medium rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200',
            'style': {}
        },
        'button_secondary': {
            'class_name': 'px-4 py-2 bg-gray-200 text-gray-800 font-medium rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200',
            'style': {}
        },
        'checkbox': {
            'class_name': 'flex items-center space-x-2',
            'style': {}
        },
        'checkbox_input': {
            'class_name': 'w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 focus:ring-2',
            'style': {}
        },
        'checkbox_label': {
            'class_name': 'text-sm font-medium text-gray-700 cursor-pointer',
            'style': {}
        },
        'div': {
            'style': {}
        },
        'div_container': {
            'class_name': 'max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-lg',
            'style': {}
        },
        'div_flex': {
            'class_name': 'flex flex-wrap gap-4 items-center',
            'style': {}
        },
        'div_grid': {
            'class_name': 'grid grid-cols-1 md:grid-cols-2 gap-4',
            'style': {}
        },
        'field_group': {
            'class_name': 'space-y-2',
            'style': {}
        },
        'field_group_inline': {
            'class_name': 'flex flex-wrap gap-4 items-center',
            'style': {}
        },
        'form': {
            'class_name': 'space-y-6 p-6 bg-white rounded-lg shadow-md',
            'style': {}
        },
        'form_inline': {
            'class_name': 'flex flex-wrap gap-4 items-end p-4 bg-gray-50 rounded-lg',
            'style': {}
        },
        'input': {
            'class_name': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200',
            'style': {}
        },
        'label': {
            'class_name': 'block text-sm font-medium text-gray-700 mb-1',
            'style': {}
        },
        'radio': {
            'class_name': 'flex items-center space-x-2',
            'style': {}
        },
        'radio_input': {
            'class_name': 'w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500 focus:ring-2',
            'style': {}
        },
        'radio_label': {
            'class_name': 'text-sm font-medium text-gray-700 cursor-pointer',
            'style': {}
        },
        'select': {
            'class_name': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white transition duration-200',
            'style': {}
        },
        'span': {
            'class_name': 'inline-block',
            'style': {}
        },
        'span_badge': {
            'class_name': 'inline-block px-2 py-1 text-xs font-semibold text-blue-800 bg-blue-100 rounded-full',
            'style': {}
        },
        'span_error': {
            'class_name': 'inline-block text-sm text-red-600 mt-1',
            'style': {}
        },
        'textarea': {
            'class_name': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-vertical transition duration-200',
            'style': {}
        }
    }

    @classmethod
    def get_style(cls, component_type: str, variant: str = None) -> Dict[str, Any]:
        """
        Obtém o estilo para um componente
        
        Args:
            component_type: Tipo do componente (input, button, etc.)
            variant: Variante do componente (secondary, danger, etc.)
        
        Returns:
            Dict com class_name e style
        """
        key = component_type
        if variant:
            key = f"{component_type}_{variant}"
        
        return cls.DEFAULT_STYLES.get(key, cls.DEFAULT_STYLES.get(component_type, {'class_name': '', 'style': {}}))
    
    @classmethod
    def register_style(cls, component_type: str, class_name: str, style: Dict = None, variant: str = None):
        """
        Registra um novo estilo ou sobrescreve um existente
        
        Args:
            component_type: Tipo do componente
            class_name: Classes CSS
            style: Estilos inline
            variant: Variante do componente
        """
        key = component_type
        if variant:
            key = f"{component_type}_{variant}"
        
        cls.DEFAULT_STYLES[key] = {
            'class_name': class_name,
            'style': style or {}
        }


class BaseComponent(ABC):
    """Classe base para todos os componentes web com injeção de dependência de estilos"""
    
    def __init__(self, style_provider: StyleProvider = None, style_variant: str = None, **kwargs):
        # Injeção de dependência do provedor de estilos
        self.style_provider = style_provider or StyleProvider()
        self.style_variant = style_variant
        
        # Obtém estilos padrão do provedor
        component_type = self.__class__.__name__.lower()
        default_styles = self.style_provider.get_style(component_type, style_variant)
        
        # Atributos globais HTML com estilos padrão
        self.id = kwargs.get('id', '')
        self.class_name = kwargs.get('class_name', default_styles.get('class_name', ''))
        self.style = {**default_styles.get('style', {}), **kwargs.get('style', {})}
        self.title = kwargs.get('title', '')
        self.lang = kwargs.get('lang', '')
        self.dir = kwargs.get('dir', '')
        self.hidden = kwargs.get('hidden', False)
        self.tab_index = kwargs.get('tab_index', 0)
        self.access_key = kwargs.get('access_key', '')
        self.content_editable = kwargs.get('content_editable', False)
        self.draggable = kwargs.get('draggable', False)
        self.spell_check = kwargs.get('spell_check', True)
        self.translate = kwargs.get('translate', True)
        self.role = kwargs.get('role', '')
        self.aria_label = kwargs.get('aria_label', '')
        self.aria_describedby = kwargs.get('aria_describedby', '')
        self.aria_labelledby = kwargs.get('aria_labelledby', '')
        self.data_attributes = kwargs.get('data_attributes', {})
        
        self.class_name += ' ' + kwargs.get('add_class_name', '')
        self.style = self.style | kwargs.get('add_style', {})

        # Eventos
        self.on_click = kwargs.get('on_click', '')
        self.on_focus = kwargs.get('on_focus', '')
        self.on_blur = kwargs.get('on_blur', '')
        self.on_key_down = kwargs.get('on_key_down', '')
        self.on_key_up = kwargs.get('on_key_up', '')
        self.on_key_press = kwargs.get('on_key_press', '')
    
    def _get_base_attributes(self) -> Dict[str, Any]:
        """Retorna os atributos base comuns a todos os componentes"""
        attrs = {}
        
        if self.id: attrs['id'] = self.id
        if self.class_name: attrs['className'] = self.class_name
        if self.style: attrs['style'] = self.style
        if self.title: attrs['title'] = self.title
        if self.lang: attrs['lang'] = self.lang
        if self.dir: attrs['dir'] = self.dir
        if self.hidden: attrs['hidden'] = self.hidden
        if self.tab_index != 0: attrs['tabIndex'] = self.tab_index
        if self.access_key: attrs['accessKey'] = self.access_key
        if self.content_editable: attrs['contentEditable'] = self.content_editable
        if self.draggable: attrs['draggable'] = self.draggable
        if not self.spell_check: attrs['spellCheck'] = self.spell_check
        if not self.translate: attrs['translate'] = self.translate
        if self.role: attrs['role'] = self.role
        if self.aria_label: attrs['ariaLabel'] = self.aria_label
        if self.aria_describedby: attrs['ariaDescribedBy'] = self.aria_describedby
        if self.aria_labelledby: attrs['ariaLabelledBy'] = self.aria_labelledby
        if self.data_attributes: attrs['dataAttributes'] = self.data_attributes
        
        # Eventos
        if self.on_click: attrs['onClick'] = self.on_click
        if self.on_focus: attrs['onFocus'] = self.on_focus
        if self.on_blur: attrs['onBlur'] = self.on_blur
        if self.on_key_down: attrs['onKeyDown'] = self.on_key_down
        if self.on_key_up: attrs['onKeyUp'] = self.on_key_up
        if self.on_key_press: attrs['onKeyPress'] = self.on_key_press
        
        return attrs
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Converte o componente para dicionário"""
        pass
    
    def to_json(self, indent: int = 2) -> str:
        """Converte o componente para JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


class Input(BaseComponent):
    """Componente Input com estilos padrão"""
    
    def __init__(self, style_provider: StyleProvider = None, style_variant: str = None, **kwargs):
        super().__init__(style_provider, style_variant, **kwargs)
        
        # Atributos específicos do input
        self.type = kwargs.get('type', 'text')
        self.value = kwargs.get('value', '')
        self.placeholder = kwargs.get('placeholder', '')
        self.name = kwargs.get('name', '')
        self.disabled = kwargs.get('disabled', False)
        self.readonly = kwargs.get('readonly', False)
        self.required = kwargs.get('required', False)
        self.autofocus = kwargs.get('autofocus', False)
        self.autocomplete = kwargs.get('autocomplete', 'off')
        self.max_length = kwargs.get('max_length', None)
        self.min_length = kwargs.get('min_length', None)
        self.max = kwargs.get('max', '')
        self.min = kwargs.get('min', '')
        self.step = kwargs.get('step', '')
        self.pattern = kwargs.get('pattern', '')
        self.size = kwargs.get('size', 20)
        self.multiple = kwargs.get('multiple', False)
        self.accept = kwargs.get('accept', '')
        self.capture = kwargs.get('capture', '')
        self.form = kwargs.get('form', '')
        self.form_action = kwargs.get('form_action', '')
        self.form_enctype = kwargs.get('form_enctype', '')
        self.form_method = kwargs.get('form_method', '')
        self.form_novalidate = kwargs.get('form_novalidate', False)
        self.form_target = kwargs.get('form_target', '')
        self.list = kwargs.get('list', '')
        self.checked = kwargs.get('checked', False)
        
        # Eventos específicos
        self.on_change = kwargs.get('on_change', '')
        self.on_input = kwargs.get('on_input', '')
    
    def to_dict(self) -> Dict[str, Any]:
        attrs = self._get_base_attributes()
        
        attrs.update({
            'type': self.type,
            'value': self.value,
            'placeholder': self.placeholder,
            'name': self.name,
            'disabled': self.disabled,
            'readonly': self.readonly,
            'required': self.required,
            'autofocus': self.autofocus,
            'autocomplete': self.autocomplete,
            'size': self.size,
            'multiple': self.multiple,
            'checked': self.checked
        })
        
        if self.max_length is not None: attrs['maxLength'] = self.max_length
        if self.min_length is not None: attrs['minLength'] = self.min_length
        if self.max: attrs['max'] = self.max
        if self.min: attrs['min'] = self.min
        if self.step: attrs['step'] = self.step
        if self.pattern: attrs['pattern'] = self.pattern
        if self.accept: attrs['accept'] = self.accept
        if self.capture: attrs['capture'] = self.capture
        if self.form: attrs['form'] = self.form
        if self.form_action: attrs['formAction'] = self.form_action
        if self.form_enctype: attrs['formEncType'] = self.form_enctype
        if self.form_method: attrs['formMethod'] = self.form_method
        if self.form_novalidate: attrs['formNoValidate'] = self.form_novalidate
        if self.form_target: attrs['formTarget'] = self.form_target
        if self.list: attrs['list'] = self.list
        if self.on_change: attrs['onChange'] = self.on_change
        if self.on_input: attrs['onInput'] = self.on_input
        
        return {
            'type': 'input',
            'attributes': attrs
        }


class Select(BaseComponent):
    """Componente Select com estilos padrão"""
    
    def __init__(self, style_provider: StyleProvider = None, style_variant: str = None, **kwargs):
        super().__init__(style_provider, style_variant, **kwargs)
        
        self.name = kwargs.get('name', '')
        self.disabled = kwargs.get('disabled', False)
        self.required = kwargs.get('required', False)
        self.autofocus = kwargs.get('autofocus', False)
        self.multiple = kwargs.get('multiple', False)
        self.size = kwargs.get('size', 1)
        self.form = kwargs.get('form', '')
        
        # Eventos específicos
        self.on_change = kwargs.get('on_change', '')
        
        # Lista de opções
        self.options = kwargs.get('options', [])
    
    def add_option(self, value: str, text: str, selected: bool = False, disabled: bool = False):
        """Adiciona uma opção ao select"""
        option = Option(value=value, selected=selected, disabled=disabled, text=text)
        self.options.append(option)
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        attrs = self._get_base_attributes()
        
        attrs.update({
            'name': self.name,
            'disabled': self.disabled,
            'required': self.required,
            'autofocus': self.autofocus,
            'multiple': self.multiple,
            'size': self.size
        })
        
        if self.form: attrs['form'] = self.form
        if self.on_change: attrs['onChange'] = self.on_change
        
        return {
            'type': 'select',
            'attributes': attrs,
            'options': [option.to_dict() for option in self.options]
        }


class Option:
    """Componente Option para Select"""
    
    def __init__(self, value: str = '', text: str = '', selected: bool = False, disabled: bool = False):
        self.value = value
        self.text = text
        self.selected = selected
        self.disabled = disabled
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'option',
            'attributes': {
                'value': self.value,
                'selected': self.selected,
                'disabled': self.disabled
            },
            'content': self.text
        }


class Textarea(BaseComponent):
    """Componente Textarea com estilos padrão"""
    
    def __init__(self, style_provider: StyleProvider = None, style_variant: str = None, **kwargs):
        super().__init__(style_provider, style_variant, **kwargs)
        
        self.name = kwargs.get('name', '')
        self.disabled = kwargs.get('disabled', False)
        self.readonly = kwargs.get('readonly', False)
        self.required = kwargs.get('required', False)
        self.autofocus = kwargs.get('autofocus', False)
        self.placeholder = kwargs.get('placeholder', '')
        self.rows = kwargs.get('rows', 2)
        self.cols = kwargs.get('cols', 20)
        self.max_length = kwargs.get('max_length', None)
        self.min_length = kwargs.get('min_length', None)
        self.wrap = kwargs.get('wrap', 'soft')
        self.autocomplete = kwargs.get('autocomplete', 'off')
        self.form = kwargs.get('form', '')
        self.content = kwargs.get('content', '')
        
        # Eventos específicos
        self.on_change = kwargs.get('on_change', '')
        self.on_input = kwargs.get('on_input', '')
        self.on_scroll = kwargs.get('on_scroll', '')
    
    def to_dict(self) -> Dict[str, Any]:
        attrs = self._get_base_attributes()
        
        attrs.update({
            'name': self.name,
            'disabled': self.disabled,
            'readonly': self.readonly,
            'required': self.required,
            'autofocus': self.autofocus,
            'placeholder': self.placeholder,
            'rows': self.rows,
            'cols': self.cols,
            'wrap': self.wrap,
            'autocomplete': self.autocomplete
        })
        
        if self.max_length is not None: attrs['maxLength'] = self.max_length
        if self.min_length is not None: attrs['minLength'] = self.min_length
        if self.form: attrs['form'] = self.form
        if self.on_change: attrs['onChange'] = self.on_change
        if self.on_input: attrs['onInput'] = self.on_input
        if self.on_scroll: attrs['onScroll'] = self.on_scroll
        
        return {
            'type': 'textarea',
            'attributes': attrs,
            'content': self.content
        }


class Button(BaseComponent):
    """Componente Button com estilos padrão"""
    
    def __init__(self, style_provider: StyleProvider = None, style_variant: str = None, **kwargs):
        super().__init__(style_provider, style_variant, **kwargs)
        
        self.type = kwargs.get('type', 'button')
        self.name = kwargs.get('name', '')
        self.value = kwargs.get('value', '')
        self.disabled = kwargs.get('disabled', False)
        self.autofocus = kwargs.get('autofocus', False)
        self.form = kwargs.get('form', '')
        self.form_action = kwargs.get('form_action', '')
        self.form_enctype = kwargs.get('form_enctype', '')
        self.form_method = kwargs.get('form_method', '')
        self.form_novalidate = kwargs.get('form_novalidate', False)
        self.form_target = kwargs.get('form_target', '')
        self.content = kwargs.get('content', 'Button')
    
    def to_dict(self) -> Dict[str, Any]:
        attrs = self._get_base_attributes()
        
        attrs.update({
            'type': self.type,
            'name': self.name,
            'value': self.value,
            'disabled': self.disabled,
            'autofocus': self.autofocus
        })
        
        if self.form: attrs['form'] = self.form
        if self.form_action: attrs['formAction'] = self.form_action
        if self.form_enctype: attrs['formEncType'] = self.form_enctype
        if self.form_method: attrs['formMethod'] = self.form_method
        if self.form_novalidate: attrs['formNoValidate'] = self.form_novalidate
        if self.form_target: attrs['formTarget'] = self.form_target
        
        return {
            'type': 'button',
            'attributes': attrs,
            'content': self.content
        }


class Label(BaseComponent):
    """Componente Label com estilos padrão"""
    
    def __init__(self, style_provider: StyleProvider = None, style_variant: str = None, **kwargs):
        super().__init__(style_provider, style_variant, **kwargs)
        
        self.html_for = kwargs.get('html_for', '')
        self.form = kwargs.get('form', '')
        self.content = kwargs.get('content', '')
    
    def to_dict(self) -> Dict[str, Any]:
        attrs = self._get_base_attributes()
        
        if self.html_for: attrs['htmlFor'] = self.html_for
        if self.form: attrs['form'] = self.form
        
        return {
            'type': 'label',
            'attributes': attrs,
            'content': self.content
        }


class Div(BaseComponent):
    """Componente Div com estilos padrão"""
    
    def __init__(self, style_provider: StyleProvider = None, style_variant: str = None, **kwargs):
        super().__init__(style_provider, style_variant, **kwargs)
        
        self.content = kwargs.get('content', '')
        self.components = kwargs.get('components', [])
    
    def add_child(self, child: BaseComponent):
        """Adiciona um componente filho"""
        self.components.append(child)
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        attrs = self._get_base_attributes()
        
        result = {
            'type': 'div',
            'attributes': attrs
        }
        
        if self.components:
            result['components'] = [child.to_dict() for child in self.components]
        
        if self.content:
            result['content'] = self.content
        
        return result


class Span(BaseComponent):
    """Componente Span com estilos padrão"""
    
    def __init__(self, style_provider: StyleProvider = None, style_variant: str = None, **kwargs):
        super().__init__(style_provider, style_variant, **kwargs)
        
        self.content = kwargs.get('content', '')
    
    def to_dict(self) -> Dict[str, Any]:
        attrs = self._get_base_attributes()
        
        return {
            'type': 'span',
            'attributes': attrs,
            'content': self.content
        }


class Form(BaseComponent):
    """Componente Form com estilos padrão"""
    
    def __init__(self, style_provider: StyleProvider = None, style_variant: str = None, **kwargs):
        super().__init__(style_provider, style_variant, **kwargs)
        
        self.action = kwargs.get('action', '')
        self.method = kwargs.get('method', 'get')
        self.enctype = kwargs.get('enctype', 'application/x-www-form-urlencoded')
        self.target = kwargs.get('target', '')
        self.accept_charset = kwargs.get('accept_charset', '')
        self.autocomplete = kwargs.get('autocomplete', 'on')
        self.novalidate = kwargs.get('novalidate', False)
        self.components = kwargs.get('components', [])
        
        # Eventos específicos
        self.on_submit = kwargs.get('on_submit', '')
        self.on_reset = kwargs.get('on_reset', '')
    
    def add_child(self, child: BaseComponent):
        """Adiciona um componente filho"""
        self.components.append(child)
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        attrs = self._get_base_attributes()
        
        attrs.update({
            'action': self.action,
            'method': self.method,
            'encType': self.enctype,
            'target': self.target,
            'acceptCharset': self.accept_charset,
            'autocomplete': self.autocomplete,
            'noValidate': self.novalidate
        })
        
        if self.on_submit: attrs['onSubmit'] = self.on_submit
        if self.on_reset: attrs['onReset'] = self.on_reset
        
        return {
            'type': 'form',
            'attributes': attrs,
            'components': [child.to_dict() for child in self.components]
        }


class Checkbox(BaseComponent):
    """Componente Checkbox com estilos padrão"""
    
    def __init__(self, style_provider: StyleProvider = None, style_variant: str = None, **kwargs):
        super().__init__(style_provider, style_variant, **kwargs)
        
        self.name = kwargs.get('name', '')
        self.value = kwargs.get('value', '')
        self.checked = kwargs.get('checked', False)
        self.disabled = kwargs.get('disabled', False)
        self.required = kwargs.get('required', False)
        self.autofocus = kwargs.get('autofocus', False)
        self.form = kwargs.get('form', '')
        self.label = kwargs.get('label', '')
        
        # Eventos específicos
        self.on_change = kwargs.get('on_change', '')
    
    def to_dict(self) -> Dict[str, Any]:
        attrs = self._get_base_attributes()
        
        attrs.update({
            'name': self.name,
            'value': self.value,
            'checked': self.checked,
            'disabled': self.disabled,
            'required': self.required,
            'autofocus': self.autofocus
        })
        
        if self.form: attrs['form'] = self.form
        if self.on_change: attrs['onChange'] = self.on_change
        
        return {
            'type': 'checkbox',
            'attributes': attrs,
            'label': self.label
        }


class Radio(BaseComponent):
    """Componente Radio com estilos padrão"""
    
    def __init__(self, style_provider: StyleProvider = None, style_variant: str = None, **kwargs):
        super().__init__(style_provider, style_variant, **kwargs)
        
        self.name = kwargs.get('name', '')
        self.value = kwargs.get('value', '')
        self.checked = kwargs.get('checked', False)
        self.disabled = kwargs.get('disabled', False)
        self.required = kwargs.get('required', False)
        self.autofocus = kwargs.get('autofocus', False)
        self.form = kwargs.get('form', '')
        self.label = kwargs.get('label', '')
        
        # Eventos específicos
        self.on_change = kwargs.get('on_change', '')
    
    def to_dict(self) -> Dict[str, Any]:
        attrs = self._get_base_attributes()
        
        attrs.update({
            'name': self.name,
            'value': self.value,
            'checked': self.checked,
            'disabled': self.disabled,
            'required': self.required,
            'autofocus': self.autofocus
        })
        
        if self.form: attrs['form'] = self.form
        if self.on_change: attrs['onChange'] = self.on_change
        
        return {
            'type': 'radio',
            'attributes': attrs,
            'label': self.label
        }


class Page(BaseComponent):
    """Componente Page com estilos padrão"""

    def __init__(self, style_provider: StyleProvider = None, style_variant: str = None, **kwargs):
        super().__init__(style_provider, style_variant, **kwargs)
        
        self.label = kwargs.get('label', '')
        self.components = kwargs.get('components', [])
        self.layout = kwargs.get('layout', '')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'page': {
                'layout': self.layout,
                'title': self.label,
                'components': [component.to_dict() for component in self.components],
            }
        }


class InputLabel(Div):
    """
    Componente composto que agrupa um Label e um Input,
    garantindo que estejam sempre conectados.
    Herda de Div para atuar como o contêiner.
    """
    def __init__(self, 
                 # Propriedades para o Label
                 label: str,
                 
                 # Propriedades para o Input (o 'name' é obrigatório)
                 name: str,
                 
                 # Outras propriedades comuns do Input (passadas via kwargs)
                 **kwargs):
        """
        Args:
            label (str): O texto que aparecerá na tag <label>.
            name (str): O atributo 'name' para a tag <input>. Usado também como 'id' se não for fornecido.
            **kwargs: Todos os outros argumentos são passados diretamente para o componente Input
                      (ex: type, placeholder, required, on_change, etc.).
                      Atributos para o Div contêiner (ex: add_class_name) podem ser passados,
                      mas geralmente o estilo padrão de 'field_group' é suficiente.
        """
        # 1. Inicializa o Div contêiner. Usamos o estilo 'field_group' para um espaçamento padrão.
        super().__init__(style_variant='field_group')

        # 2. Determina o ID do input. É crucial para conectar o label.
        #    Se o usuário não passar um 'id', usamos o 'name' como um padrão seguro.
        input_id = kwargs.get('id', name)

        # 3. Cria o componente Label, associando-o ao input através de 'html_for'.
        label_component = Label(content=label, html_for=input_id)
        
        # 4. Assegura que o 'name' e o 'id' estão no dicionário de props do input.
        input_props = kwargs.copy()
        input_props['name'] = name
        input_props['id'] = input_id

        # 5. Cria o componente Input com todas as propriedades recebidas.
        input_component = Input(**input_props)
        
        # 6. Adiciona o Label e o Input como filhos do Div contêiner.
        self.add_child(label_component)
        self.add_child(input_component)


# Exemplo de uso
def get_example():
    # Criando um formulário completo
    form = Form(
        id="user-form",
        add_class_name="form-container",
        method="post",
        action="/submit-user",
        on_submit="handleSubmit"
    )
    
    # Grupo Nome
    name_group = Div(add_class_name="form-group")
    name_input = InputLabel(
        id="name",
        name="name",
        type="text",
        label="Nome:",
        add_class_name="form-control",
        placeholder="Digite seu nome",
        required=True,
        max_length=100,
        on_change="handleNameChange"
    )
    name_group.add_child(name_input)
    
    # Grupo Email
    email_group = Div(add_class_name="form-group")
    email_input = InputLabel(
        id="email",
        name="email",
        type="email",
        label="Email:",
        add_class_name="form-control",
        placeholder="Digite seu email",
        required=True,
        on_change="handleEmailChange"
    )
    email_group.add_child(email_input)
    
    # Grupo País
    country_group = Div(add_class_name="form-group")
    country_label = Label(html_for="country", add_class_name="form-label", content="País:")
    country_select = Select(
        id="country",
        name="country",
        add_class_name="form-control",
        required=True,
        on_change="handleCountryChange"
    )
    country_select.add_option("", "Selecione um país", selected=True)
    country_select.add_option("br", "Brasil")
    country_select.add_option("us", "Estados Unidos")
    country_group.add_child(country_label).add_child(country_select)
    
    # Grupo Bio
    bio_group = Div(add_class_name="form-group")
    bio_label = Label(html_for="bio", add_class_name="form-label", content="Bio:")
    bio_textarea = Textarea(
        id="bio",
        name="bio",
        add_class_name="form-control",
        placeholder="Conte um pouco sobre você",
        rows=4,
        max_length=500,
        on_change="handleBioChange"
    )
    bio_group.add_child(bio_label).add_child(bio_textarea)
    
    # Checkbox
    newsletter_group = Div(add_class_name="form-group !mt-2")
    newsletter_checkbox = Checkbox(
        id="newsletter",
        name="newsletter",
        value="yes",
        label="Quero receber newsletter",
        on_change="handleNewsletterChange"
    )
    newsletter_group.add_child(newsletter_checkbox)
    
    # Botões
    actions_group = Div(add_class_name="form-actions space-x-1")
    submit_button = Button(
        type="submit",
        content="Enviar",
        on_click="handleSubmitClick"
    )
    reset_button = Button(
        type="reset",
        style_variant="secondary",
        content="Limpar",
        on_click="handleResetClick"
    )
    actions_group.add_child(submit_button).add_child(reset_button)
    
    # Montando o formulário
    form.add_child(name_group)
    form.add_child(email_group)
    form.add_child(country_group)
    form.add_child(bio_group)
    form.add_child(newsletter_group)
    form.add_child(actions_group)
    
    page = Page(label='Titulo', components=[form])
    # Gerando o JSON
    # print("JSON gerado pelo backend:")
    # print(form.to_json())
    return page.to_json()