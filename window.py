# Se importa sistema
import sys
# Se importa gi como libreria base
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio, GObject

# Clase del mensaje
class Mensaje(Gtk.MessageDialog):
    def __init__(self, parent):
        super().__init__(title="Mensaje")
        self.add_buttons(
            "_OK",
            Gtk.ResponseType.OK
        )
        self.set_markup("Se guardado el texto")

# Clase base de la ventana de la aplicacion
class Ventana(Gtk.ApplicationWindow):
    # Definicion de como va a ser la ventana
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Parametros base (Tamaño, Titulo)
        self.set_default_size(800, 250)
        self.set_title("VENTANA")
        # Contenedores base
        self.box1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        # Coloca la caja
        self.set_child(self.box1)
        # Coloca label en la caja
        self.label = Gtk.Label()
        self.box1.append(self.label)
        self.label.set_text("En esta apliacion puedes guardar texto")
        # Coloca la entrada del texto en la caja
        self.texto = Gtk.Entry()
        self.box1.append(self.texto)
        # Añade ek boton save
        self.button_save = Gtk.Button(label="Guardar")
        self.button_save.connect('clicked', self.save)
        self.box1.append(self.button_save)
        # atributos para el guardado
        self._native1 = self.dialog_save()
        self._native1.connect("response", self.on_file_save_response)

    # Funcion(Dialog guardar)
    def dialog_save(self): 
        return Gtk.FileChooserNative(title="Save File",
                                    action=Gtk.FileChooserAction.SAVE,
                                    accept_label="_Guardar",
                                    cancel_label="_Cancelar",
                                    )

    # Funcion(guardando)
    def on_file_save_response(self, native, response):
        if response == Gtk.ResponseType.ACCEPT:
            _path = native.get_file().get_path()
            print(_path)
            with open(_path, "w") as _file:
                _file.write(f'{self.texto.get_text()}\n')
                self.mostrar_mensaje()

    # Funcion(save)
    def save(self, button):
        self._native1.show()

    # Funcion(mostrar mensaje)
    def mostrar_mensaje(self):
        msn = Mensaje(parent=self.get_root())
        msn.set_visible(True)
        msn.connect("response", self.respuesta_ok)

    # Funcion(Concetar respuesta)
    def respuesta_ok(self, m, response):
        if response == Gtk.ResponseType.OK:
            print("Se guardo")
        self.close()

# Clase de la aplicacion
class Aplicacion(Gtk.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)


    def on_activate(self, app):
        self.win = Ventana(application=app)
        self.win.present()


app = Aplicacion(application_id="com.example.GtkApplication")
app.run(sys.argv)
