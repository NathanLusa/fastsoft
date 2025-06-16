"""
Sistema de Componentes Web em Python
Gera JSON para renderização no frontend
"""

import json
from typing import Dict, List, Any, Optional, Union
from abc import ABC, abstractmethod


class BaseComponent(ABC):
    """Classe base para todos os componentes web"""
    
    def __init__(self, **kwargs):
        # Atributos globais HTML
        self.id = kwargs.get('id', '')
        self.class_name = kwargs.get('class_name', '')  # class no HTML
        self.style = kwargs.get('style', {})
        self.title = kwargs.get('title', '')
        self.lang = kwargs.get('lang', '')
        self.dir = kwargs.get('dir', '')  # ltr, rtl, auto
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
    """Componente Input"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
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
    """Componente Select"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
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
    """Componente Textarea"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
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
        self.wrap = kwargs.get('wrap', 'soft')  # hard, soft, off
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
    """Componente Button"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.type = kwargs.get('type', 'button')  # button, submit, reset
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
    """Componente Label"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.html_for = kwargs.get('html_for', '')  # for no HTML
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
    """Componente Div"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
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
    """Componente Span"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.content = kwargs.get('content', '')
    
    def to_dict(self) -> Dict[str, Any]:
        attrs = self._get_base_attributes()
        
        return {
            'type': 'span',
            'attributes': attrs,
            'content': self.content
        }


class Form(BaseComponent):
    """Componente Form"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.action = kwargs.get('action', '')
        self.method = kwargs.get('method', 'get')  # get, post
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
    """Componente Checkbox (wrapper para input type checkbox)"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
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
    """Componente Radio (wrapper para input type radio)"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.label = kwargs.get('label', '')
        self.components = kwargs.get('components', [])

    def to_dict(self) -> Dict[str, Any]:
        # attrs = self._get_base_attributes()
        
        # attrs.update({
        #     'name': self.name,
        #     'value': self.value,
        #     'checked': self.checked,
        #     'disabled': self.disabled,
        #     'required': self.required,
        #     'autofocus': self.autofocus
        # })
        
        # if self.form: attrs['form'] = self.form
        # if self.on_change: attrs['onChange'] = self.on_change
        
        return {
            'page': {
                'layout': 'grid',
                'title': self.label,
                'components': [component.to_dict() for component in self.components],
            }
        }

# Exemplo de uso
def get_example():
    # Criando um formulário completo
    form = Form(
        id="user-form",
        class_name="form-container",
        method="post",
        action="/submit-user",
        on_submit="handleSubmit"
    )
    
    # Grupo Nome
    name_group = Div(class_name="form-group")
    name_label = Label(html_for="name", class_name="form-label", content="Nome:")
    name_input = Input(
        id="name",
        name="name",
        type="text",
        class_name="form-control",
        placeholder="Digite seu nome",
        required=True,
        max_length=100,
        on_change="handleNameChange"
    )
    name_group.add_child(name_label).add_child(name_input)
    
    # Grupo Email
    email_group = Div(class_name="form-group")
    email_label = Label(html_for="email", class_name="form-label", content="Email:")
    email_input = Input(
        id="email",
        name="email",
        type="email",
        class_name="form-control",
        placeholder="Digite seu email",
        required=True,
        on_change="handleEmailChange"
    )
    email_group.add_child(email_label).add_child(email_input)
    
    # Grupo País
    country_group = Div(class_name="form-group")
    country_label = Label(html_for="country", class_name="form-label", content="País:")
    country_select = Select(
        id="country",
        name="country",
        class_name="form-control",
        required=True,
        on_change="handleCountryChange"
    )
    country_select.add_option("", "Selecione um país", selected=True)
    country_select.add_option("br", "Brasil")
    country_select.add_option("us", "Estados Unidos")
    country_group.add_child(country_label).add_child(country_select)
    
    # Grupo Bio
    bio_group = Div(class_name="form-group")
    bio_label = Label(html_for="bio", class_name="form-label", content="Bio:")
    bio_textarea = Textarea(
        id="bio",
        name="bio",
        class_name="form-control",
        placeholder="Conte um pouco sobre você",
        rows=4,
        max_length=500,
        on_change="handleBioChange"
    )
    bio_group.add_child(bio_label).add_child(bio_textarea)
    
    # Checkbox
    newsletter_group = Div(class_name="form-group")
    newsletter_checkbox = Checkbox(
        id="newsletter",
        name="newsletter",
        value="yes",
        label="Quero receber newsletter",
        on_change="handleNewsletterChange"
    )
    newsletter_group.add_child(newsletter_checkbox)
    
    # Botões
    actions_group = Div(class_name="form-actions")
    submit_button = Button(
        type="submit",
        class_name="btn btn-primary",
        content="Enviar",
        on_click="handleSubmitClick"
    )
    reset_button = Button(
        type="reset",
        class_name="btn btn-secondary",
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