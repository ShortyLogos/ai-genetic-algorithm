
import sys

import gaapp
import boite_vue
import optimisation_geometrique

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QFileDialog
from __feature__ import snake_case, true_property
QFileDialog.getSaveFileName = QFileDialog.get_save_file_name


if __name__ == '__main__':
    
    QApplication.set_attribute(Qt.AA_EnableHighDpiScaling, True)

    app = QApplication(sys.argv)
    ga_app = gaapp.QGAApp()

    # ajout de vos stratégies
    # -------------------------------------------------------- par exemple
    # ga_app.add_crossover_strategy(my_awesome_strategy)
    # ga_app.add_mutation_strategy(ma_spectaculaire_strategie)

    # ajout de vos panneaux de résolution de problème
    # -------------------------------------------------------- par exemple
    ga_app.add_solution_panel(boite_vue.BoxPanel())
    ga_app.add_solution_panel(optimisation_geometrique.ShapePanel())
    # ga_app.add_solution_panel(probleme_3)

    ga_app.show()
    sys.exit(app.exec_())

