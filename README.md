# QMLearn website

Static documentation site for [QMLearn](https://github.com/Quantum-MultiScale/QMLearn): quantum machine learning of 1- and 2-electron reduced density matrices.

Design follows the [Quantum Multiscale](https://github.com/Quantum-MultiScale/quantum-multiscale) site layout with a **blue, red, and black** color palette.

## Preview locally

```bash
cd docs
python3 -m http.server 8080
```

Open [http://localhost:8080](http://localhost:8080).

## Structure

| Page | Description |
|------|-------------|
| `index.html` | Home, overview, papers, contributors |
| `install.html` | Requirements and GitHub / pip install |
| `tutorials.html` | 1-/2-RDM training, AIMD notebooks, and YouTube talks |
| `source.html` | QMMol, QMModel, QMLCalculator, I/O |
| `contact.html` | Developers, GitHub, citations |
| `notebooks/` | Tutorial notebooks and AIMD example scripts |

## Deploy

The site is published from the `docs/` folder on the `main` branch via [GitHub Pages](https://pages.github.com/) at [qmlearn.rutgers.edu](https://qmlearn.rutgers.edu/). No build step is required; `docs/.nojekyll` ensures static assets under `_static/` are served as-is.
