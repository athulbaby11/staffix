const viewMoreJobsButton = document.querySelector("#view-more-jobs");
const extraJobs = document.querySelectorAll(".extra-job");
const menuToggle = document.querySelector(".menu-toggle");
const navigationLinks = document.querySelector(".nav-links");
const siteHeader = document.querySelector(".site-header");

if (siteHeader) {
    const updateHeaderOnScroll = () => {
        siteHeader.classList.toggle("is-scrolled", window.scrollY > 30);
    };

    updateHeaderOnScroll();
    window.addEventListener("scroll", updateHeaderOnScroll, { passive: true });
}

if (viewMoreJobsButton) {
    viewMoreJobsButton.addEventListener("click", () => {
        extraJobs.forEach((job) => job.classList.add("visible"));
        viewMoreJobsButton.hidden = true;
    });
}

if (menuToggle && navigationLinks) {
    menuToggle.addEventListener("click", () => {
        const isOpen = navigationLinks.classList.toggle("is-open");
        menuToggle.setAttribute("aria-expanded", String(isOpen));
        menuToggle.setAttribute("aria-label", isOpen ? "Close navigation menu" : "Open navigation menu");
        menuToggle.innerHTML = `<i class="bi ${isOpen ? "bi-x-lg" : "bi-list"}"></i>`;
    });

    navigationLinks.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", () => {
            navigationLinks.classList.remove("is-open");
            menuToggle.setAttribute("aria-expanded", "false");
            menuToggle.setAttribute("aria-label", "Open navigation menu");
            menuToggle.innerHTML = '<i class="bi bi-list"></i>';
        });
    });
}

const jobSearch = document.querySelector("#job-search");
const jobLocation = document.querySelector("#job-location");
const jobTypeFilter = document.querySelector("#job-type-filter");
const jobEmploymentFilter = document.querySelector("#job-employment-filter");
const jobCards = Array.from(document.querySelectorAll(".job-card"));
const jobResults = document.querySelector("#job-results");
const noJobs = document.querySelector("#no-jobs");

function filterJobs() {
    const search = (jobSearch?.value || "").trim().toLowerCase();
    const location = jobLocation?.value || "";
    const type = jobTypeFilter?.value || "";
    const employment = jobEmploymentFilter?.value || "";
    let visibleJobs = 0;

    jobCards.forEach((card) => {
        const matchesSearch = !search || `${card.dataset.title} ${card.dataset.company}`.toLowerCase().includes(search);
        const matchesLocation = !location || card.dataset.location === location;
        const matchesType = !type || card.dataset.type === type;
        const matchesEmployment = !employment || card.dataset.employment === employment;
        const isVisible = matchesSearch && matchesLocation && matchesType && matchesEmployment;
        card.hidden = !isVisible;
        if (isVisible) visibleJobs += 1;
    });

    if (jobResults) jobResults.textContent = `${visibleJobs} ${visibleJobs === 1 ? "role" : "roles"} available`;
    if (noJobs) noJobs.hidden = visibleJobs !== 0;
}

[jobSearch, jobLocation, jobTypeFilter, jobEmploymentFilter].forEach((filter) => filter?.addEventListener("input", filterJobs));
filterJobs();

const applicationModal = document.querySelector("#application-modal");
const applicationForm = document.querySelector("#application-form");
const applicationFormView = document.querySelector("#application-form-view");
const applicationSuccess = document.querySelector("#application-success");
const selectedJob = document.querySelector("#selected-job");

function closeApplication() {
    if (!applicationModal) return;
    applicationModal.hidden = true;
    document.body.style.overflow = "";
    applicationForm?.reset();
    if (applicationFormView) applicationFormView.hidden = false;
    if (applicationSuccess) applicationSuccess.hidden = true;
}

document.querySelectorAll(".job-apply").forEach((button) => {
    button.addEventListener("click", () => {
        if (!applicationModal) return;
        if (selectedJob) selectedJob.textContent = button.dataset.job || "this role";
        applicationModal.hidden = false;
        document.body.style.overflow = "hidden";
        applicationForm?.querySelector("input")?.focus();
    });
});

document.querySelectorAll("[data-close-application]").forEach((element) => element.addEventListener("click", closeApplication));
applicationForm?.addEventListener("submit", (event) => {
    event.preventDefault();
    if (applicationFormView) applicationFormView.hidden = true;
    if (applicationSuccess) applicationSuccess.hidden = false;
});
document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && applicationModal && !applicationModal.hidden) closeApplication();
});

const revealItems = document.querySelectorAll(".hero-content, .hero-card, .intro, .solutions, .process, .industries, .why-us, .jobs, .mission, .testimonial, .contact, .contact-details");

revealItems.forEach((item) => item.setAttribute("data-reveal", ""));

const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
    });
}, { threshold: 0.12 });

revealItems.forEach((item) => revealObserver.observe(item));

const hero = document.querySelector(".hero");
const heroCard = document.querySelector(".hero-card");
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

if (hero && heroCard && !prefersReducedMotion) {
    hero.addEventListener("pointermove", (event) => {
        const bounds = hero.getBoundingClientRect();
        const x = (event.clientX - bounds.left) / bounds.width - 0.5;
        const y = (event.clientY - bounds.top) / bounds.height - 0.5;
        heroCard.style.transform = `perspective(900px) rotateY(${x * 5}deg) rotateX(${y * -5}deg)`;
    });

    hero.addEventListener("pointerleave", () => {
        heroCard.style.transform = "";
    });
}
