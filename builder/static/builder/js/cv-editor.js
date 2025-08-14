// CV Editor JavaScript
class CVEditor {
    constructor() {
        this.sections = [];
        this.currentTemplate = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.setupAutoSave();
    }

    bindEvents() {
        // Template selection
        document.addEventListener('click', (e) => {
            if (e.target.closest('.template-card')) {
                this.selectTemplate(e.target.closest('.template-card'));
            }
        });

        // Add section
        document.getElementById('add-section')?.addEventListener('click', () => {
            this.addSection();
        });

        // Save CV
        document.getElementById('save-cv')?.addEventListener('click', () => {
            this.saveCV();
        });

        // Export PDF
        document.getElementById('export-pdf')?.addEventListener('click', () => {
            this.exportPDF();
        });
    }

    selectTemplate(templateCard) {
        document.querySelectorAll('.template-card').forEach(card => {
            card.classList.remove('active');
        });
        templateCard.classList.add('active');
        this.currentTemplate = templateCard.dataset.templateId;
        this.updatePreview();
    }

    addSection() {
        const section = {
            id: Date.now(),
            title: 'New Section',
            content: '',
            type: 'custom'
        };
        this.sections.push(section);
        this.renderSections();
    }

    renderSections() {
        const sectionList = document.getElementById('section-list');
        if (!sectionList) return;

        sectionList.innerHTML = this.sections.map(section => `
            <div class="section-item" data-id="${section.id}">
                <h4>${section.title}</h4>
                <div class="section-controls">
                    <button onclick="cvEditor.editSection(${section.id})">Edit</button>
                    <button onclick="cvEditor.deleteSection(${section.id})">Delete</button>
                </div>
            </div>
        `).join('');
    }

    editSection(id) {
        const section = this.sections.find(s => s.id === id);
        if (!section) return;

        // Populate edit form
        document.getElementById('section-title').value = section.title;
        document.getElementById('section-content').value = section.content;
    }

    deleteSection(id) {
        this.sections = this.sections.filter(s => s.id !== id);
        this.renderSections();
        this.updatePreview();
    }

    updatePreview() {
        const preview = document.getElementById('cv-preview');
        if (!preview) return;

        let html = `<div class="cv-template ${this.currentTemplate || 'default'}">`;
        
        this.sections.forEach(section => {
            html += `
                <div class="cv-section">
                    <h2>${section.title}</h2>
                    <div class="section-content">${section.content}</div>
                </div>
            `;
        });
        
        html += '</div>';
        preview.innerHTML = html;
    }

    saveCV() {
        const cvData = {
            template: this.currentTemplate,
            sections: this.sections,
            title: document.getElementById('cv-title')?.value || 'Untitled CV'
        };

        fetch('/api/save-cv/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken()
            },
            body: JSON.stringify(cvData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('CV saved successfully!');
            }
        });
    }

    exportPDF() {
        window.open(`/api/export-pdf/${this.cvId || 'new'}/`, '_blank');
    }

    setupAutoSave() {
        setInterval(() => {
            if (this.sections.length > 0) {
                this.saveCV();
            }
        }, 30000); // Auto-save every 30 seconds
    }

    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }
}

// Initialize CV Editor
const cvEditor = new CVEditor();

// Global functions for template access
window.editSection = (id) => cvEditor.editSection(id);
window.deleteSection = (id) => cvEditor.deleteSection(id);
