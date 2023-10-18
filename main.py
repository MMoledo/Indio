import sys
from lista import lista
import numpy as np  # para dados de teste
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QWidget
from PyQt5.QtGui import QFont
import pyqtgraph as pg
from PyQt5.QtGui import QRegion, QPainterPath
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurando estilos globais
        self.setStyleSheet("background-color: #111111; color: #FFFFFF;")

        # Cabeçalho (Header)
        headerPanel = QWidget(self)
        headerPanel.setStyleSheet("background-color: #252525; padding: 10px; ")
        headerPanel.setMaximumHeight(100)  # Defina a altura máxima desejada
        headerLayout = QHBoxLayout(headerPanel)

        # Título do Dashboard
        title = QLabel("Gráficos | PRODES", self)
        titleFont = QFont("Arial", 20)
        titleFont.setBold(True)  # Aplicar negrito
        title.setFont(titleFont)
        headerLayout.addWidget(title)

        # Seleção Território
        territoryLabel = QLabel("Selecionar Território:", self)
        territoryLabelFont = QFont("Arial", 12)
        territoryLabelFont.setBold(True)  # Aplicar negrito
        territoryLabel.setFont(territoryLabelFont)
        territorySelection = QComboBox(self)
        territorySelectionFont = QFont("Arial", 8)  # Fonte para o texto do dropdown
        territorySelectionFont.setBold(True)  # Aplicar negrito
        territorySelection.setFont(territorySelectionFont)
        territorySelection.addItems(lista)
        territorySelection.setMaximumWidth(150)

        # Usar um QHBoxLayout para alinhar horizontalmente o rótulo e a seleção
        territoryLayout = QHBoxLayout()
        territoryLayout.addWidget(territoryLabel)
        territoryLayout.addWidget(territorySelection)
        headerLayout.addLayout(territoryLayout)


        # Seleção Território
        dataLabel = QLabel("Selecione período:", self)
        dataLabelFont = QFont("Arial", 12)
        dataLabelFont.setBold(True)  # Aplicar negrito
        dataLabel.setFont(dataLabelFont)
        dataSelection = QComboBox(self)
        dataSelectionFont = QFont("Arial", 12)  # Fonte para o texto do dropdown
        dataSelectionFont.setBold(True)  # Aplicar negrito
        dataSelection.setFont(dataSelectionFont)
        dataSelection.addItems(["Todos","2019", "2020", "2021", "2022"])
        dataSelection.setMaximumWidth(100)

        # Usar um QHBoxLayout para alinhar horizontalmente o rótulo e a seleção
        dataLayout = QHBoxLayout()
        dataLayout.addWidget(dataLabel)
        dataLayout.addWidget(dataSelection) 
        headerLayout.addLayout(dataLayout)

        # Filtro
        filterButton = QPushButton("Filtrar", self)
        filterButtonFont = QFont("Arial", 12)
        filterButtonFont.setBold(True)  # Aplicar negrito
        filterButton.setFont(filterButtonFont)
        filterButton.setMaximumWidth(100)
        filterButton.setStyleSheet("background-color: #7FC71A; color: #FFFFFF; border-radius: 5px;")
        headerLayout.addWidget(filterButton)

        # Definindo o layout do cabeçalho na janela principal
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(headerPanel)
        centralWidget = QWidget(self)
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

        # Configurações da janela
        self.setGeometry(100, 100, 1200, 600)
        self.setWindowTitle('Dashboard')

        # Definindo o layout do cabeçalho na janela principal
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(headerPanel)

        centralWidget = QWidget(self)
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)
        card1 = self.createCard("Desmatamento Terras Indígenas\n1,1 milhões de ha")
        card2 = self.createCard("Desmatamento TI - 2010\n294.7 Km²")
        card3 = self.createCard("Maior Índice - Estado - 2010\nPará – 3.312 Km²")

        # Adicionando cartões à layout principal
        cardLayout = QHBoxLayout()
        cardLayout.addWidget(card1)
        cardLayout.addWidget(card2)
        cardLayout.addWidget(card3)

        # Criando o 1 Grafico
        x = np.array([1, 2, 3, 4, 5])
        height = np.array([2, 4, 6, 8, 3])

        # Chamando a função para criar o gráfico de colunas 
        barGraphWidget = self.createBarGraph(x, height)
        
        # Ajustando o tamanho do widget do gráfico
        barGraphWidget.setMinimumSize(400, 200)
        barGraphWidget.setMaximumSize(400, 200)
        cardLayout.addWidget(barGraphWidget)
        mainLayout.addLayout(cardLayout)
        
        # Adicionando o gráfico de colunas ao layout principal
        graphLayout = QHBoxLayout()
        x = np.array([1, 2, 3, 4, 5])
        height = np.array([2, 4, 6, 8, 3])

        # Chamando a função para criar o gráfico de colunas
        barGraphWidget = self.createBarGraph(x, height)
        
        # Ajustando o tamanho do widget do gráfico
        barGraphWidget.setMinimumSize(800, 200)
        barGraphWidget.setMaximumSize(800, 200)
        
        # Adicionando o gráfico de colunas ao layout principal
        graphLayout.addWidget(barGraphWidget)
        labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
        sizes = [15, 30, 45, 10]

        # Criar o widget do gráfico de pizza
        pieChartWidget = self.createPieChart(labels, sizes)

        # Ajustando o tamanho do widget do gráfico
        pieChartWidget.setMinimumSize(400, 200)
        pieChartWidget.setMaximumSize(400, 200)

        # Adicionar o gráfico de pizza ao layout principal
        graphLayout.addWidget(pieChartWidget)
        mainLayout.addLayout(graphLayout)


        self.territorySelection = territorySelection
        self.dataSelection = dataSelection

        # Conecte o botão 'Filtrar' à função on_filter_clicked
        filterButton.clicked.connect(self.on_filter_clicked)

    def on_filter_clicked(self):
        print(self.territorySelection.currentText())
        print(self.dataSelection.currentText())


    def createCard(self, text):
        """ Função para criar um card simples """
        card = QWidget(self)
        card.setMaximumSize(300, 200)  # Defina o tamanho máximo dos cards
        cardLayout = QVBoxLayout(card)
        
        card.setStyleSheet("""
            background-color: #333333; 
            border-radius: 8px; 
            padding: 10px; 
            margin: 10px;
        """)
        
        # Adicionando texto ao card
        label = QLabel(text, self)
        labelFont = QFont("Arial", 10)
        labelFont.setBold(True)  # Aplicar negrito
        label.setFont(labelFont)
        cardLayout.addWidget(label)
        
        return card
    
    def createBarGraph(self, x, height):
        """Função para criar um gráfico de colunas."""
        
        # Criar o gráfico de colunas com fundo personalizado
        barGraphWidget = pg.PlotWidget(self, background='#333333')
        
        # Ajustar a cor do texto e dos eixos do gráfico
        axis = barGraphWidget.getAxis('left')
        axis.setTextPen('#FFFFFF')
        axis.setPen('#FFFFFF')
        axis = barGraphWidget.getAxis('bottom')
        axis.setTextPen('#FFFFFF')
        axis.setPen('#FFFFFF')

        # Adicionar os dados ao gráfico de colunas
        barGraphWidget.plot(x, height, pen='#7FC71A', fillLevel=0, brush=(127, 199, 26, 150))
        
        return barGraphWidget
    
    def createPieChart(self, labels, sizes):
        """Função para criar um gráfico de pizza usando Matplotlib e incorporá-lo ao PyQt."""
        fig = Figure(figsize=(5, 5), dpi=100)
        ax = fig.add_subplot(111)
        fig.patch.set_facecolor('#333333')
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#7FC71A', '#3498db', '#e74c3c', '#34495e'])
        ax.axis('equal')  # Equal aspect ratio garante que a pizza seja desenhada como um círculo.

        # Criar o widget do gráfico de pizza
        pieWidget = FigureCanvas(fig)
        pieWidget.setStyleSheet("background-color:transparent;")

        return pieWidget
    
    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec_())
