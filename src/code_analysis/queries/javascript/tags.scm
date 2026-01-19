; tags.scm for JavaScript symbol extraction

; Function declarations
(function_declaration
  name: (identifier) @name @definition.function)

; Class declarations
(class_declaration
  name: (identifier) @name @definition.class)

; Arrow functions assigned to const/let (lexical_declaration)
(lexical_declaration
  (variable_declarator
    name: (identifier) @name
    value: (arrow_function)) @definition.function)

; Arrow functions assigned to var (variable_declaration)
(variable_declaration
  (variable_declarator
    name: (identifier) @name
    value: (arrow_function)) @definition.function)

; Regular functions assigned to const/let
(lexical_declaration
  (variable_declarator
    name: (identifier) @name
    value: (function_expression)) @definition.function)

; Regular functions assigned to var
(variable_declaration
  (variable_declarator
    name: (identifier) @name
    value: (function_expression)) @definition.function)

; Exported arrow functions (export const/let)
(export_statement
  declaration: (lexical_declaration
    (variable_declarator
      name: (identifier) @name
      value: (arrow_function)) @definition.function))

; Exported function declarations
(export_statement
  declaration: (function_declaration
    name: (identifier) @name @definition.function))

; Exported class declarations
(export_statement
  declaration: (class_declaration
    name: (identifier) @name @definition.class))

; Class methods
(class_body
  (method_definition
    name: (property_identifier) @name @definition.method))

; Generator functions
(generator_function_declaration
  name: (identifier) @name @definition.function)
