document.addEventListener('DOMContentLoaded', function () {
    console.log("CV form script loaded"); // Debugging log

    // Form validation
    const form = document.getElementById('cv-form');
    if (!form) {
        console.error("CV form not found!"); // Debugging log
        return;
    }
    form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.classList.add('was-validated');
    }, false);

    // Character count for summary
    const summary = document.getElementById('summary');
    const summaryCount = document.getElementById('summary-count');
    if (summary) {
        summary.addEventListener('input', () => {
            summaryCount.textContent = summary.value.length;
        });
    } else {
        console.error("Summary field not found!"); // Debugging log
    }

    // Template selection
    document.querySelectorAll('.template-card').forEach(card => {
        card.addEventListener('click', () => {
            document.querySelectorAll('.template-card').forEach(c => c.classList.remove('active'));
            card.classList.add('active');
            document.getElementById('template_id').value = card.dataset.templateId;
        });
    });

    // Dynamic sections
    window.addExperience = function () {
        const container = document.getElementById('experience-container');
        const index = container.children.length;
        const template = `
            <div class="card mb-3 experience-entry">
                <div class="card-body">
                    <div class="d-flex justify-content-between">
                        <h5>Experience #${index + 1}</h5>
                        <button type="button" class="btn-close" onclick="this.closest('.experience-entry').remove()"></button>
                    </div>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Job Title</label>
                            <input type="text" name="experience[${index}][job_title]" class="form-control">
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Company</label>
                            <input type="text" name="experience[${index}][company]" class="form-control">
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Start Date</label>
                            <input type="month" name="experience[${index}][start_date]" class="form-control">
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">End Date</label>
                            <input type="month" name="experience[${index}][end_date]" class="form-control">
                        </div>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Description</label>
                        <textarea name="experience[${index}][description]" class="form-control" rows="3"></textarea>
                    </div>
                </div>
            </div>
        `;
        container.insertAdjacentHTML('beforeend', template);
    };

    window.addEducation = function () {
        const container = document.getElementById('education-container');
        const index = container.children.length;
        const template = `
            <div class="card mb-3 education-entry">
                <div class="card-body">
                    <div class="d-flex justify-content-between">
                        <h5>Education #${index + 1}</h5>
                        <button type="button" class="btn-close" onclick="this.closest('.education-entry').remove()"></button>
                    </div>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Degree</label>
                            <input type="text" name="education[${index}][degree]" class="form-control">
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">School</label>
                            <input type="text" name="education[${index}][school]" class="form-control">
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Graduation Year</label>
                            <input type="number" name="education[${index}][graduation_year]" class="form-control">
                        </div>
                    </div>
                </div>
            </div>
        `;
        container.insertAdjacentHTML('beforeend', template);
    };

    // Skills input
    const skillsInput = document.getElementById('skills-input');
    const skillsContainer = document.getElementById('skills-container');
    if (skillsInput) {
        skillsInput.addEventListener('keydown', (e) => {
            if (e.key === ',' || e.key === 'Enter') {
                e.preventDefault();
                const skill = skillsInput.value.trim();
                if (skill) {
                    const tag = `
                        <span class="badge bg-primary">
                            ${skill}
                            <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
                        </span>
                    `;
                    skillsContainer.insertAdjacentHTML('beforeend', tag);
                    skillsInput.value = '';
                }
            }
        });
    } else {
        console.error("Skills input not found!"); // Debugging log
    }

    // Auto-save functionality (to localStorage)
    form.addEventListener('input', () => {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        localStorage.setItem('cvFormData', JSON.stringify(data));
    });

    // Load from localStorage
    const savedData = localStorage.getItem('cvFormData');
    if (savedData) {
        const data = JSON.parse(savedData);
        for (const key in data) {
            if (form.elements[key]) {
                form.elements[key].value = data[key];
            }
        }
    }
});
