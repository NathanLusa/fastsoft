"""
FormBuilder - Facilita a criação de formulários usando os componentes web
"""

from typing import Dict, List, Any, Optional
from backend.components import *


class FormBuilder:
    """Builder para facilitar a criação de formulários"""
    
    def __init__(self, form_id: str = "", class_name: str = "", action: str = "", method: str = "post"):
        self.form = Form(
            id=form_id,
            class_name=class_name,
            action=action,
            method=method
        )
        self.current_group = None
    
    def start_group(self, class_name: str = "form-group") -> 'FormBuilder':
        """Inicia um novo grupo de campos"""
        self.current_group = Div(class_name=class_name)
        return self
    
    def end_group(self) -> 'FormBuilder':
        """Finaliza o grupo atual e adiciona ao formulário"""
        if self.current_group:
            self.form.add_child(self.current_group)
            self.current_group = None
        return self
    
    def add_text_field(self, 
                      field_id: str,
                      label_text: str,
                      name: str = None,
                      placeholder: str = "",
                      required: bool = False,
                      max_length: int = None,
                      class_name: str = "form-control") -> 'FormBuilder':
        """Adiciona um campo de texto com label"""
        if not self.current_group:
            self.start_group()
        
        name = name or field_id
        
        label = Label(html_for=field_id, class_name="form-label", content=label_text)
        input_field = Input(
            id=field_id,
            name=name,
            type="text",
            class_name=class_name,
            placeholder=placeholder,
            required=required,
            max_length=max_length
        )
        
        self.current_group.add_child(label).add_child(input_field)
        return self
    
    def add_email_field(self,
                       field_id: str,
                       label_text: str,
                       name: str = None,
                       placeholder: str = "",
                       required: bool = False,
                       class_name: str = "form-control") -> 'FormBuilder':
        """Adiciona um campo de email com label"""
        if not self.current_group:
            self.start_group()
        
        name = name or field_id
        
        label = Label(html_for=field_id, class_name="form-label", content=label_text)
        input_field = Input(
            id=field_id,
            name=name,
            type="email",
            class_name=class_name,
            placeholder=placeholder,
            required=required
        )
        
        self.current_group.add_child(label).add_child(input_field)
        return self
    
    def add_password_field(self,
                          field_id: str,
                          label_text: str,
                          name: str = None,
                          placeholder: str = "",
                          required: bool = False,
                          min_length: int = None,
                          class_name: str = "form-control") -> 'FormBuilder':
        """Adiciona um campo de senha com label"""
        if not self.current_group:
            self.start_group()
        
        name = name or field_id
        
        label = Label(html_for=field_id, class_name="form-label", content=label_text)
        input_field = Input(
            id=field_id,
            name=name,
            type="password",
            class_name=class_name,
            placeholder=placeholder,
            required=required,
            min_length=min_length
        )
        
        self.current_group.add_child(label).add_child(input_field)
        return self
    
    # def add_number_field(self,
    #                     field_id: str,
    #                     label_text: str,
    #                     name: str = None,
    #                     placeholder: str = "",
    #                     required: bool = False,
    #                     min_val: float = None,
    #                     max_val: float = None,
    #                     step: float = None,
    #                     class_name: str = "form-control") -> 'FormBuilder':
    #     """Adiciona um campo numérico com label"""
    #     if not self.current_group:
    #         self.start_group()
        
    #     name = name or field_id
        
    #     label = Label(html_for=field_id, class_name="form-label", content=label_text)
    #     input_field = Input(
    #         id=field_id,
    #         name=name,
    #         type="number",
    #         class_name=class_name,
    #         placeholder=placeholder,
    #         required=required,
    #         min=str(min_val) if min_val is not None else "",