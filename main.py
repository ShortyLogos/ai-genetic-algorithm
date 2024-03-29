
import sys

import gaapp
import box_vue
import shape_vue
import community_vue
import model.custom_strategies as cs

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QFileDialog
from __feature__ import snake_case, true_property
QFileDialog.getSaveFileName = QFileDialog.get_save_file_name


if __name__ == '__main__':
    
    QApplication.set_attribute(Qt.AA_EnableHighDpiScaling, True)

    app = QApplication(sys.argv)
    ga_app = gaapp.QGAApp()

    # ajout de panneaux de résolution de problème
    ga_app.add_solution_panel(box_vue.BoxPanel())
    ga_app.add_solution_panel(shape_vue.ShapePanel())
    ga_app.add_solution_panel(community_vue.CommunityPanel())

    # ajout de stratégies de mutation personnalisées
    ga_app.add_mutation_strategy(cs.WildGenesStrategy)

    ga_app.show()
    sys.exit(app.exec_())

