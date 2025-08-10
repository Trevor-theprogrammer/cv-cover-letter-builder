// CV Template Functionality
class CVTemplateEditor {
  constructor() {
    this.init();
  }

  init() {
    this.bindEditableElements();
    this.setupAutoSave();
  }

  bindEditableElements() {
    const editableElements = document.querySelectorAll(
      '[contenteditable="true"]'
    );

    editableElements.forEach((element) => {
      element.addEventListener('blur', () => this.handleContentChange(element));
      element.addEventListener('keydown', (e) =>
        this.handleKeyPress(e, element)
      );
    });
  }

  setupAutoSave() {
    let timeout = null;
    const editableElements = document.querySelectorAll(
      '[contenteditable="true"]'
    );

    editableElements.forEach((element) => {
      element.addEventListener('input', () => {
        clearTimeout(timeout);
        timeout = setTimeout(() => this.saveChanges(), 1000);
      });
    });
  }

  handleContentChange(element) {
    // Get element identifier (could be a data attribute or class)
    const elementId = element.getAttribute('data-field') || element.className;
    const content = element.innerHTML;

    // Trigger save
    this.saveChanges({
      [elementId]: content,
    });
  }

  handleKeyPress(e, element) {
    // Handle special key combinations
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      // Insert a new line break instead of a div
      document.execCommand('insertLineBreak');
    }
  }

  async saveChanges(data = null) {
    if (!data) {
      data = this.collectAllContent();
    }

    try {
      const response = await fetch('/builder/cv/save-draft/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCsrfToken(),
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error('Failed to save changes');
      }

      console.log('Changes saved successfully');
    } catch (error) {
      console.error('Error saving changes:', error);
      // Could add user notification here
    }
  }

  collectAllContent() {
    const content = {};
    const editableElements = document.querySelectorAll(
      '[contenteditable="true"]'
    );

    editableElements.forEach((element) => {
      const elementId = element.getAttribute('data-field') || element.className;
      content[elementId] = element.innerHTML;
    });

    return content;
  }

  getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
  }

  // Add methods for adding/removing sections if needed
  addSection(sectionType) {
    // Implementation for adding new sections
  }

  removeSection(sectionElement) {
    // Implementation for removing sections
  }
}

// Initialize when the DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.cvEditor = new CVTemplateEditor();
});
