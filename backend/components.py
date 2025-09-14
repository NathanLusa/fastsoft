import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union


class StyleProvider:
    """Provedor de estilos padrão usando Tailwind CSS."""
    
    DEFAULT_STYLES = {
        'button': {
            'class_name': (
                'px-4 py-2 bg-blue-600 text-white font-medium rounded-md '
                'hover:bg-blue-700 focus:outline-none focus:ring-2 '
                'focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 '
                'disabled:cursor-not-allowed transition duration-200'
            ),
            'style': {}
        },
        'button_danger': {
            'class_name': (
                'px-4 py-2 bg-red-600 text-white font-medium rounded-md '
                'hover:bg-red-700 focus:outline-none focus:ring-2 '
                'focus:ring-red-500 focus:ring-offset-2 disabled:opacity-50 '
                'disabled:cursor-not-allowed transition duration-200'
            ),
            'style': {}
        },
        'button_secondary': {
            'class_name': (
                'px-4 py-2 bg-gray-200 text-gray-800 font-medium rounded-md '
                'hover:bg-gray-300 focus:outline-none focus:ring-2 '
                'focus:ring-gray-500 focus:ring-offset-2 disabled:opacity-50 '
                'disabled:cursor-not-allowed transition duration-200'
            ),
            'style': {}
        },
        'checkbox': {
            'class_name': 'flex items-center space-x-2',
            'style': {}
        },
        'checkbox_input': {
            'class_name': (
                'w-4 h-4 text-blue-600 border-gray-300 rounded '
                'focus:ring-blue-500 focus:ring-2'
            ),
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
            'class_name': (
                'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm '
                'focus:outline-none focus:ring-2 focus:ring-blue-500 '
                'focus:border-blue-500 transition duration-200'
            ),
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
            'class_name': (
                'w-4 h-4 text-blue-600 border-gray-300 '
                'focus:ring-blue-500 focus:ring-2'
            ),
            'style': {}
        },
        'radio_label': {
            'class_name': 'text-sm font-medium text-gray-700 cursor-pointer',
            'style': {}
        },
        'select': {
            'class_name': (
                'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm '
                'focus:outline-none focus:ring-2 focus:ring-blue-500 '
                'focus:border-blue-500 bg-white transition duration-200'
            ),
            'style': {}
        },
        'span': {
            'class_name': 'inline-block',
            'style': {}
        },
        'span_badge': {
            'class_name': (
                'inline-block px-2 py-1 text-xs font-semibold '
                'text-blue-800 bg-blue-100 rounded-full'
            ),
            'style': {}
        },
        'span_error': {
            'class_name': 'inline-block text-sm text-red-600 mt-1',
            'style': {}
        },
        'textarea': {
            'class_name': (
                'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm '
                'focus:outline-none focus:ring-2 focus:ring-blue-500 '
                'focus:border-blue-500 resize-vertical transition duration-200'
            ),
            'style': {}
        },
        'fieldset': {
            'class_name': 'border border-gray-300 rounded-md p-4 space-y-4',
            'style': {}
        },
        'legend': {
            'class_name': 'text-sm font-medium text-gray-700 px-2',
            'style': {}
        },
        'img': {
            'class_name': 'max-w-full h-auto rounded-md',
            'style': {}
        },
        'a': {
            'class_name': 'text-blue-600 hover:text-blue-800 underline',
            'style': {}
        },
        'h1': {
            'class_name': 'text-3xl font-bold text-gray-900 mb-4',
            'style': {}
        },
        'h2': {
            'class_name': 'text-2xl font-bold text-gray-900 mb-3',
            'style': {}
        },
        'h3': {
            'class_name': 'text-xl font-bold text-gray-900 mb-2',
            'style': {}
        },
        'h4': {
            'class_name': 'text-lg font-bold text-gray-900 mb-2',
            'style': {}
        },
        'h5': {
            'class_name': 'text-base font-bold text-gray-900 mb-1',
            'style': {}
        },
        'h6': {
            'class_name': 'text-sm font-bold text-gray-900 mb-1',
            'style': {}
        },
        'p': {
            'class_name': 'text-gray-700 mb-2',
            'style': {}
        }
    }

    @classmethod
    def get_style(cls, component_type: str, variant: str = None) -> Dict[str, Any]:
        """
        Obtém o estilo para um componente.
        
        Args:
            component_type: Tipo do componente (input, button, etc.)
            variant: Variante do componente (secondary, danger, etc.)
        
        Returns:
            Dict com class_name e style
        """
        key = component_type
        if variant:
            key = f"{component_type}_{variant}"
        
        default_style = {'class_name': '', 'style': {}}
        return cls.DEFAULT_STYLES.get(
            key, 
            cls.DEFAULT_STYLES.get(component_type, default_style)
        )
    
    @classmethod
    def register_style(cls, component_type: str, class_name: str, 
                      style: Dict = None, variant: str = None):
        """
        Registra um novo estilo ou sobrescreve um existente.
        
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
    
    @classmethod
    def get_all_styles(cls) -> Dict[str, Dict[str, Any]]:
        """Retorna todos os estilos registrados."""
        return cls.DEFAULT_STYLES.copy()
    
    @classmethod
    def has_style(cls, component_type: str, variant: str = None) -> bool:
        """Verifica se um estilo existe."""
        key = component_type
        if variant:
            key = f"{component_type}_{variant}"
        return key in cls.DEFAULT_STYLES
    
    @classmethod
    def remove_style(cls, component_type: str, variant: str = None) -> bool:
        """
        Remove um estilo registrado.
        
        Returns:
            True se o estilo foi removido, False se não existia
        """
        key = component_type
        if variant:
            key = f"{component_type}_{variant}"
        
        if key in cls.DEFAULT_STYLES:
            del cls.DEFAULT_STYLES[key]
            return True
        return False
    
    @classmethod
    def validate_class_name(cls, class_name: str) -> bool:
        """Valida se a class_name contém apenas classes Tailwind válidas."""
        # Validação básica - pode ser expandida
        if not isinstance(class_name, str):
            return False
        
        # Verifica se não contém caracteres perigosos
        dangerous_chars = ['<', '>', '"', "'", ';', '(', ')']
        return not any(char in class_name for char in dangerous_chars)


class BaseComponent(ABC):
    """Classe base para todos os componentes web com injeção de dependência de estilos."""
    
    def __init__(self, style_provider: StyleProvider = None, 
                 style_variant: str = None, **kwargs):
        # Injeção de dependência do provedor de estilos
        self.style_provider = style_provider or StyleProvider()
        self.style_variant = style_variant
        
        # Obtém estilos padrão do provedor
        component_type = self.__class__.__name__.lower()
        default_styles = self.style_provider.get_style(
            component_type, style_variant
        )
        
        # Atributos globais HTML com estilos padrão
        self.id = kwargs.get('id', '')
        self.class_name = kwargs.get(
            'class_name', 
            default_styles.get('class_name', '')
        )
        self.style = {
            **default_styles.get('style', {}), 
            **kwargs.get('style', {})
        }
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
        """Retorna os atributos base comuns a todos os componentes."""
        attrs = {}
        
        if self.id:
            attrs['id'] = self.id
        if self.class_name:
            attrs['className'] = self.class_name
        if self.style:
            attrs['style'] = self.style
        if self.title:
            attrs['title'] = self.title
        if self.lang:
            attrs['lang'] = self.lang
        if self.dir:
            attrs['dir'] = self.dir
        if self.hidden:
            attrs['hidden'] = self.hidden
        if self.tab_index != 0:
            attrs['tabIndex'] = self.tab_index
        if self.access_key:
            attrs['accessKey'] = self.access_key
        if self.content_editable:
            attrs['contentEditable'] = self.content_editable
        if self.draggable:
            attrs['draggable'] = self.draggable
        if not self.spell_check:
            attrs['spellCheck'] = self.spell_check
        if not self.translate:
            attrs['translate'] = self.translate
        if self.role:
            attrs['role'] = self.role
        if self.aria_label:
            attrs['ariaLabel'] = self.aria_label
        if self.aria_describedby:
            attrs['ariaDescribedBy'] = self.aria_describedby
        if self.aria_labelledby:
            attrs['ariaLabelledBy'] = self.aria_labelledby
        if self.data_attributes:
            attrs['dataAttributes'] = self.data_attributes
        
        # Eventos
        if self.on_click:
            attrs['onClick'] = self.on_click
        if self.on_focus:
            attrs['onFocus'] = self.on_focus
        if self.on_blur:
            attrs['onBlur'] = self.on_blur
        if self.on_key_down:
            attrs['onKeyDown'] = self.on_key_down
        if self.on_key_up:
            attrs['onKeyUp'] = self.on_key_up
        if self.on_key_press:
            attrs['onKeyPress'] = self.on_key_press
        
        return attrs
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Converte o componente para dicionário."""
        pass
    
    def to_json(self, indent: int = 2) -> str:
        """Converte o componente para JSON."""
        return json.dumps(
            self.to_dict(), 
            ensure_ascii=False, 
            indent=indent
        )
    
    def add_class(self, class_name: str) -> 'BaseComponent':
        """Adiciona uma classe CSS ao componente."""
        if class_name and class_name not in self.class_name:
            self.class_name += f' {class_name}'
        return self
    
    def remove_class(self, class_name: str) -> 'BaseComponent':
        """Remove uma classe CSS do componente."""
        if class_name in self.class_name:
            self.class_name = self.class_name.replace(f' {class_name}', '')
            self.class_name = self.class_name.replace(class_name, '')
        return self
    
    def set_style(self, property_name: str, value: str) -> 'BaseComponent':
        """Define um estilo inline no componente."""
        self.style[property_name] = value
        return self
    
    def remove_style(self, property_name: str) -> 'BaseComponent':
        """Remove um estilo inline do componente."""
        if property_name in self.style:
            del self.style[property_name]
        return self
    
    def set_attribute(self, attr_name: str, value: Any) -> 'BaseComponent':
        """Define um atributo HTML no componente."""
        setattr(self, attr_name, value)
        return self
    
    def get_attribute(self, attr_name: str, default: Any = None) -> Any:
        """Obtém um atributo HTML do componente."""
        return getattr(self, attr_name, default)
    
    def validate_required_attributes(self, required_attrs: List[str]) -> bool:
        """Valida se os atributos obrigatórios estão presentes."""
        for attr in required_attrs:
            if not hasattr(self, attr) or not getattr(self, attr):
                return False
        return True


class Input(BaseComponent):
    """Componente Input com estilos padrão."""
    
    def __init__(self, style_provider: StyleProvider = None, 
                 style_variant: str = None, **kwargs):
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
        
        if self.max_length is not None:
            attrs['maxLength'] = self.max_length
        if self.min_length is not None:
            attrs['minLength'] = self.min_length
        if self.max:
            attrs['max'] = self.max
        if self.min:
            attrs['min'] = self.min
        if self.step:
            attrs['step'] = self.step
        if self.pattern:
            attrs['pattern'] = self.pattern
        if self.accept:
            attrs['accept'] = self.accept
        if self.capture:
            attrs['capture'] = self.capture
        if self.form:
            attrs['form'] = self.form
        if self.form_action:
            attrs['formAction'] = self.form_action
        if self.form_enctype:
            attrs['formEncType'] = self.form_enctype
        if self.form_method:
            attrs['formMethod'] = self.form_method
        if self.form_novalidate:
            attrs['formNoValidate'] = self.form_novalidate
        if self.form_target:
            attrs['formTarget'] = self.form_target
        if self.list:
            attrs['list'] = self.list
        if self.on_change:
            attrs['onChange'] = self.on_change
        if self.on_input:
            attrs['onInput'] = self.on_input
        
        return {
            'type': 'input',
            'attributes': attrs
        }


class Select(BaseComponent):
    """Componente Select com estilos padrão."""
    
    def __init__(self, style_provider: StyleProvider = None, 
                 style_variant: str = None, **kwargs):
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
    
    def add_option(self, value: str, text: str, selected: bool = False, 
                   disabled: bool = False):
        """Adiciona uma opção ao select."""
        option = Option(
            value=value, 
            selected=selected, 
            disabled=disabled, 
            text=text
        )
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
        
        if self.form:
            attrs['form'] = self.form
        if self.on_change:
            attrs['onChange'] = self.on_change
        
        return {
            'type': 'select',
            'attributes': attrs,
            'options': [option.to_dict() for option in self.options]
        }


class Option:
    """Componente Option para Select."""
    
    def __init__(self, value: str = '', text: str = '', 
                 selected: bool = False, disabled: bool = False):
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
    """Componente Textarea com estilos padrão."""
    
    def __init__(self, style_provider: StyleProvider = None, 
                 style_variant: str = None, **kwargs):
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
        
        if self.max_length is not None:
            attrs['maxLength'] = self.max_length
        if self.min_length is not None:
            attrs['minLength'] = self.min_length
        if self.form:
            attrs['form'] = self.form
        if self.on_change:
            attrs['onChange'] = self.on_change
        if self.on_input:
            attrs['onInput'] = self.on_input
        if self.on_scroll:
            attrs['onScroll'] = self.on_scroll
        
        return {
            'type': 'textarea',
            'attributes': attrs,
            'content': self.content
        }


class Button(BaseComponent):
    """Componente Button com estilos padrão."""
    
    def __init__(self, style_provider: StyleProvider = None, 
                 style_variant: str = None, **kwargs):
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
        
        if self.form:
            attrs['form'] = self.form
        if self.form_action:
            attrs['formAction'] = self.form_action
        if self.form_enctype:
            attrs['formEncType'] = self.form_enctype
        if self.form_method:
            attrs['formMethod'] = self.form_method
        if self.form_novalidate:
            attrs['formNoValidate'] = self.form_novalidate
        if self.form_target:
            attrs['formTarget'] = self.form_target
        
        return {
            'type': 'button',
            'attributes': attrs,
            'content': self.content
        }


class Label(BaseComponent):
    """Componente Label com estilos padrão."""
    
    def __init__(self, style_provider: StyleProvider = None, 
                 style_variant: str = None, **kwargs):
        super().__init__(style_provider, style_variant, **kwargs)
        
        self.html_for = kwargs.get('html_for', '')
        self.form = kwargs.get('form', '')
        self.content = kwargs.get('content', '')
    
    def to_dict(self) -> Dict[str, Any]:
        attrs = self._get_base_attributes()
        
        if self.html_for:
            attrs['htmlFor'] = self.html_for
        if self.form:
            attrs['form'] = self.form
        
        return {
            'type': 'label',
            'attributes': attrs,
            'content': self.content
        }


class Div(BaseComponent):
    """Componente Div com estilos padrão."""
    
    def __init__(self, style_provider: StyleProvider = None, 
                 style_variant: str = None, **kwargs):
        super().__init__(style_provider, style_variant, **kwargs)
        
        self.content = kwargs.get('content', '')
        self.components = kwargs.get('components', [])
    
    def add_child(self, child: BaseComponent):
        """Adiciona um componente filho."""
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
    """Componente Span com estilos padrão."""
    
    def __init__(self, style_provider: StyleProvider = None, 
                 style_variant: str = None, **kwargs):
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
    """Componente Form com estilos padrão."""
    
    def __init__(self, style_provider: StyleProvider = None, 
                 style_variant: str = None, **kwargs):
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
        """Adiciona um componente filho."""
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
        
        if self.on_submit:
            attrs['onSubmit'] = self.on_submit
        if self.on_reset:
            attrs['onReset'] = self.on_reset
        
        return {
            'type': 'form',
            'attributes': attrs,
            'components': [child.to_dict() for child in self.components]
        }


class Checkbox(BaseComponent):
    """Componente Checkbox com estilos padrão."""
    
    def __init__(self, style_provider: StyleProvider = None, 
                 style_variant: str = None, **kwargs):
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
        
        if self.form:
            attrs['form'] = self.form
        if self.on_change:
            attrs['onChange'] = self.on_change
        
        return {
            'type': 'checkbox',
            'attributes': attrs,
            'label': self.label
        }


class Radio(BaseComponent):
    """Componente Radio com estilos padrão."""
    
    def __init__(self, style_provider: StyleProvider = None, 
                 style_variant: str = None, **kwargs):
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
        
        if self.form:
            attrs['form'] = self.form
        if self.on_change:
            attrs['onChange'] = self.on_change
        
        return {
            'type': 'radio',
            'attributes': attrs,
            'label': self.label
        }


class Fieldset(BaseComponent):
    """Componente Fieldset para agrupar elementos de formulário."""
    
    def __init__(self, style_provider: StyleProvider = None, 
                 style_variant: str = None, **kwargs):
        super().__init__(style_provider, style_variant, **kwargs)
        
        self.legend = kwargs.get('legend', '')
        self.disabled = kwargs.get('disabled', False)
        self.form = kwargs.get('form', '')
        self.components = kwargs.get('components', [])
    
    def add_child(self, child: BaseComponent):
        """Adiciona um componente filho."""
        self.components.append(child)
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        attrs = self._get_base_attributes()
        
        if self.disabled:
            attrs['disabled'] = self.disabled
        if self.form:
            attrs['form'] = self.form
        
        result = {
            'type': 'fieldset',
            'attributes': attrs,
            'legend': self.legend,
            'components': [child.to_dict() for child in self.components]
        }
        
        return result


class Legend(BaseComponent):
    """Componente Legend para Fieldset."""
    
    def __init__(self, style_provider: StyleProvider = None, 
                 style_variant: str = None, **kwargs):
        super().__init__(style_provider, style_variant, **kwargs)
        
        self.content = kwargs.get('content', '')
    
    def to_dict(self) -> Dict[str, Any]:
        attrs = self._get_base_attributes()
        
        return {
            'type': 'legend',
            'attributes': attrs,
            'content': self.content
        }


class Image(BaseComponent):
    """Componente Image com estilos padrão."""
    
    def __init__(self, style_provider: StyleProvider = None, 
                 style_variant: str = None, **kwargs):
        super().__init__(style_provider, style_variant, **kwargs)
        
        self.src = kwargs.get('src', '')
        self.alt = kwargs.get('alt', '')
        self.width = kwargs.get('width', None)
        self.height = kwargs.get('height', None)
        self.loading = kwargs.get('loading', 'lazy')
        self.cross_origin = kwargs.get('cross_origin', '')
        self.use_map = kwargs.get('use_map', '')
        self.is_map = kwargs.get('is_map', False)
        self.decoding = kwargs.get('decoding', 'async')
        self.fetch_priority = kwargs.get('fetch_priority', '')
        
        # Eventos específicos
        self.on_load = kwargs.get('on_load', '')
        self.on_error = kwargs.get('on_error', '')
    
    def to_dict(self) -> Dict[str, Any]:
        attrs = self._get_base_attributes()
        
        attrs.update({
            'src': self.src,
            'alt': self.alt,
            'loading': self.loading,
            'decoding': self.decoding
        })
        
        if self.width is not None:
            attrs['width'] = self.width
        if self.height is not None:
            attrs['height'] = self.height
        if self.cross_origin:
            attrs['crossOrigin'] = self.cross_origin
        if self.use_map:
            attrs['useMap'] = self.use_map
        if self.is_map:
            attrs['isMap'] = self.is_map
        if self.fetch_priority:
            attrs['fetchPriority'] = self.fetch_priority
        if self.on_load:
            attrs['onLoad'] = self.on_load
        if self.on_error:
            attrs['onError'] = self.on_error
        
        return {
            'type': 'img',
            'attributes': attrs
        }


class Link(BaseComponent):
    """Componente Link (anchor) com estilos padrão."""
    
    def __init__(self, style_provider: StyleProvider = None, 
                 style_variant: str = None, **kwargs):
        super().__init__(style_provider, style_variant, **kwargs)
        
        self.href = kwargs.get('href', '')
        self.target = kwargs.get('target', '')
        self.rel = kwargs.get('rel', '')
        self.download = kwargs.get('download', '')
        self.hreflang = kwargs.get('hreflang', '')
        self.type = kwargs.get('type', '')
        self.content = kwargs.get('content', '')
    
    def to_dict(self) -> Dict[str, Any]:
        attrs = self._get_base_attributes()
        
        attrs.update({
            'href': self.href
        })
        
        if self.target:
            attrs['target'] = self.target
        if self.rel:
            attrs['rel'] = self.rel
        if self.download:
            attrs['download'] = self.download
        if self.hreflang:
            attrs['hreflang'] = self.hreflang
        if self.type:
            attrs['type'] = self.type
        
        return {
            'type': 'a',
            'attributes': attrs,
            'content': self.content
        }


class Heading(BaseComponent):
    """Componente Heading (h1-h6) com estilos padrão."""
    
    def __init__(self, level: int = 1, style_provider: StyleProvider = None, 
                 style_variant: str = None, **kwargs):
        super().__init__(style_provider, style_variant, **kwargs)
        
        self.level = max(1, min(6, level))  # Garante que seja entre 1 e 6
        self.content = kwargs.get('content', '')
    
    def to_dict(self) -> Dict[str, Any]:
        attrs = self._get_base_attributes()
        
        return {
            'type': f'h{self.level}',
            'attributes': attrs,
            'content': self.content
        }


class Paragraph(BaseComponent):
    """Componente Paragraph com estilos padrão."""
    
    def __init__(self, style_provider: StyleProvider = None, 
                 style_variant: str = None, **kwargs):
        super().__init__(style_provider, style_variant, **kwargs)
        
        self.content = kwargs.get('content', '')
    
    def to_dict(self) -> Dict[str, Any]:
        attrs = self._get_base_attributes()
        
        return {
            'type': 'p',
            'attributes': attrs,
            'content': self.content
        }


class Page(BaseComponent):
    """Componente Page com estilos padrão."""

    def __init__(self, style_provider: StyleProvider = None, 
                 style_variant: str = None, **kwargs):
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
            name (str): O atributo 'name' para a tag <input>. 
                        Usado também como 'id' se não for fornecido.
            **kwargs: Todos os outros argumentos são passados diretamente 
                      para o componente Input (ex: type, placeholder, required, 
                      on_change, etc.). Atributos para o Div contêiner 
                      (ex: add_class_name) podem ser passados, mas geralmente 
                      o estilo padrão de 'field_group' é suficiente.
        """
        # 1. Inicializa o Div contêiner. Usamos o estilo 'field_group' 
        # para um espaçamento padrão.
        super().__init__(style_variant='field_group')

        # 2. Determina o ID do input. É crucial para conectar o label.
        #    Se o usuário não passar um 'id', usamos o 'name' como um 
        #    padrão seguro.
        input_id = kwargs.get('id', name)

        # 3. Cria o componente Label, associando-o ao input através 
        #    de 'html_for'.
        label_component = Label(content=label, html_for=input_id)
        
        # 4. Assegura que o 'name' e o 'id' estão no dicionário de 
        #    props do input.
        input_props = kwargs.copy()
        input_props['name'] = name
        input_props['id'] = input_id

        # 5. Cria o componente Input com todas as propriedades 
        #    recebidas.
        input_component = Input(**input_props)
        
        # 6. Adiciona o Label e o Input como filhos do Div contêiner.
        self.add_child(label_component)
        self.add_child(input_component)
    
    def get_input(self) -> Input:
        """Retorna o componente Input."""
        return self.components[1] if len(self.components) > 1 else None
    
    def get_label(self) -> Label:
        """Retorna o componente Label."""
        return self.components[0] if len(self.components) > 0 else None
    
    def set_input_value(self, value: str) -> 'InputLabel':
        """Define o valor do input."""
        input_component = self.get_input()
        if input_component:
            input_component.value = value
        return self
    
    def get_input_value(self) -> str:
        """Obtém o valor do input."""
        input_component = self.get_input()
        return input_component.value if input_component else ''
    
    def set_input_required(self, required: bool = True) -> 'InputLabel':
        """Define se o input é obrigatório."""
        input_component = self.get_input()
        if input_component:
            input_component.required = required
        return self
    
    def set_input_disabled(self, disabled: bool = True) -> 'InputLabel':
        """Define se o input está desabilitado."""
        input_component = self.get_input()
        if input_component:
            input_component.disabled = disabled
        return self


# Exemplo de uso
def get_example():
    """Exemplo de uso dos componentes."""
    # Criando uma página completa
    page = Page(
        label='Formulário de Cadastro',
        layout='single'
    )
    
    # Título da página
    title = Heading(
        level=1,
        content="Cadastro de Usuário",
        add_class_name="text-center mb-8"
    )
    
    # Descrição
    description = Paragraph(
        content="Preencha os dados abaixo para criar sua conta.",
        add_class_name="text-center text-gray-600 mb-6"
    )
    
    # Criando um formulário completo
    form = Form(
        id="user-form",
        add_class_name="space-y-6",
        method="post",
        action="/submit-user",
        on_submit="handleSubmit"
    )
    
    # Seção de dados pessoais
    personal_section = Fieldset(
        legend="Dados Pessoais",
        add_class_name="space-y-4"
    )
    
    # Grupo Nome
    name_input = InputLabel(
        label="Nome Completo:",
        name="name",
        type="text",
        placeholder="Digite seu nome completo",
        required=True,
        max_length=100,
        on_change="handleNameChange"
    )
    personal_section.add_child(name_input)
    
    # Grupo Email
    email_input = InputLabel(
        label="Email:",
        name="email",
        type="email",
        placeholder="Digite seu email",
        required=True,
        on_change="handleEmailChange"
    )
    personal_section.add_child(email_input)
    
    # Grupo Telefone
    phone_input = InputLabel(
        label="Telefone:",
        name="phone",
        type="tel",
        placeholder="(11) 99999-9999",
        on_change="handlePhoneChange"
    )
    personal_section.add_child(phone_input)
    
    # Seção de localização
    location_section = Fieldset(
        legend="Localização",
        add_class_name="space-y-4"
    )
    
    # Grupo País
    country_label = Label(
        html_for="country", 
        content="País:"
    )
    country_select = Select(
        id="country",
        name="country",
        required=True,
        on_change="handleCountryChange"
    )
    country_select.add_option("", "Selecione um país", selected=True)
    country_select.add_option("br", "Brasil")
    country_select.add_option("us", "Estados Unidos")
    country_select.add_option("ar", "Argentina")
    country_select.add_option("mx", "México")
    
    country_group = Div(add_class_name="space-y-2")
    country_group.add_child(country_label).add_child(country_select)
    location_section.add_child(country_group)
    
    # Grupo Cidade
    city_input = InputLabel(
        label="Cidade:",
        name="city",
        type="text",
        placeholder="Digite sua cidade",
        on_change="handleCityChange"
    )
    location_section.add_child(city_input)
    
    # Seção de informações adicionais
    additional_section = Fieldset(
        legend="Informações Adicionais",
        add_class_name="space-y-4"
    )
    
    # Grupo Bio
    bio_label = Label(
        html_for="bio", 
        content="Biografia:"
    )
    bio_textarea = Textarea(
        id="bio",
        name="bio",
        placeholder="Conte um pouco sobre você...",
        rows=4,
        max_length=500,
        on_change="handleBioChange"
    )
    
    bio_group = Div(add_class_name="space-y-2")
    bio_group.add_child(bio_label).add_child(bio_textarea)
    additional_section.add_child(bio_group)
    
    # Grupo de preferências
    preferences_group = Div(add_class_name="space-y-3")
    
    # Checkbox Newsletter
    newsletter_checkbox = Checkbox(
        id="newsletter",
        name="newsletter",
        value="yes",
        label="Quero receber newsletter",
        on_change="handleNewsletterChange"
    )
    preferences_group.add_child(newsletter_checkbox)
    
    # Checkbox Termos
    terms_checkbox = Checkbox(
        id="terms",
        name="terms",
        value="accepted",
        label="Aceito os termos de uso",
        required=True,
        on_change="handleTermsChange"
    )
    preferences_group.add_child(terms_checkbox)
    
    additional_section.add_child(preferences_group)
    
    # Botões de ação
    actions_group = Div(add_class_name="flex justify-end space-x-4 pt-6")
    
    submit_button = Button(
        type="submit",
        content="Cadastrar",
        style_variant="primary",
        on_click="handleSubmitClick"
    )
    
    reset_button = Button(
        type="reset",
        style_variant="secondary",
        content="Limpar",
        on_click="handleResetClick"
    )
    
    cancel_link = Link(
        href="/",
        content="Cancelar",
        add_class_name="px-4 py-2 text-gray-600 hover:text-gray-800"
    )
    
    actions_group.add_child(cancel_link)
    actions_group.add_child(reset_button)
    actions_group.add_child(submit_button)
    
    # Montando o formulário
    form.add_child(personal_section)
    form.add_child(location_section)
    form.add_child(additional_section)
    form.add_child(actions_group)
    
    # Montando a página
    page.components = [title, description, form]
    
    return page.to_json()


def get_simple_example():
    """Exemplo simples de uso dos componentes."""
    # Página simples
    page = Page(label='Página Simples')
    
    # Título
    title = Heading(level=2, content="Exemplo Simples")
    
    # Parágrafo
    paragraph = Paragraph(
        content="Este é um exemplo simples de como usar os componentes."
    )
    
    # Link
    link = Link(
        href="https://example.com",
        content="Visite nosso site",
        target="_blank"
    )
    
    # Imagem
    image = Image(
        src="https://via.placeholder.com/300x200",
        alt="Imagem de exemplo",
        add_class_name="rounded-lg shadow-md"
    )
    
    # Formulário simples
    form = Form(method="post", action="/submit")
    
    # Input com label
    email_input = InputLabel(
        label="Email:",
        name="email",
        type="email",
        required=True
    )
    
    # Botão
    submit_btn = Button(
        type="submit",
        content="Enviar",
        style_variant="primary"
    )
    
    form.add_child(email_input)
    form.add_child(submit_btn)
    
    # Montando a página
    page.components = [title, paragraph, link, image, form]
    
    return page.to_json()