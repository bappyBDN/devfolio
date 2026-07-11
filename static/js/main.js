/* =========================================================================
   DevFolio Pro — main.js
   Theme toggle (persisted), navbar scroll shadow, active-link marking,
   hero terminal typing effect, and small contact-page conveniences.
   ========================================================================= */
 
(function () {
  "use strict";
 
  var STORAGE_KEY = "devfolio-theme";
  var root = document.documentElement;
 
  /* ---------------------------------------------------------------------
     Theme: dark / light
     --------------------------------------------------------------------- */
  function getPreferredTheme() {
    var stored = window.localStorage.getItem(STORAGE_KEY);
    if (stored === "light" || stored === "dark") return stored;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
 
  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    document.querySelectorAll("[data-theme-toggle]").forEach(function (btn) {
      btn.setAttribute("aria-pressed", theme === "dark");
      var label = btn.querySelector(".knob i");
      if (label) label.className = theme === "dark" ? "bi bi-moon-stars-fill" : "bi bi-sun-fill";
    });
  }
 
  function initTheme() {
    applyTheme(getPreferredTheme());
 
    document.querySelectorAll("[data-theme-toggle]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
        window.localStorage.setItem(STORAGE_KEY, next);
        applyTheme(next);
      });
    });
  }
 
  /* ---------------------------------------------------------------------
     Navbar: shadow after scroll + mark active link by current path
     --------------------------------------------------------------------- */
  function initNavbar() {
    var nav = document.querySelector(".df-navbar");
    if (nav) {
      var onScroll = function () {
        nav.classList.toggle("is-scrolled", window.scrollY > 8);
      };
      onScroll();
      window.addEventListener("scroll", onScroll, { passive: true });
    }
 
    var path = window.location.pathname.replace(/\/$/, "") || "/";
    document.querySelectorAll(".df-nav .nav-link").forEach(function (link) {
      var linkPath = link.getAttribute("href");
      if (!linkPath) return;
      linkPath = linkPath.replace(/\/$/, "") || "/";
      if (linkPath === path) link.classList.add("active");
    });
  }
 
  /* ---------------------------------------------------------------------
     Hero terminal: reveal status lines one by one, then blink cursor
     --------------------------------------------------------------------- */
  function initHeroTerminal() {
    var lines = document.querySelectorAll("[data-term-line]");
    if (!lines.length) return;
 
    var prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (prefersReducedMotion) {
      lines.forEach(function (l) { l.style.opacity = 1; });
      return;
    }
 
    lines.forEach(function (line, i) {
      line.style.opacity = 0;
      line.style.transition = "opacity 0.35s ease";
      setTimeout(function () {
        line.style.opacity = 1;
      }, 220 * i + 150);
    });
  }
 
  /* ---------------------------------------------------------------------
     Bootstrap client-side validation feedback (contact form)
     --------------------------------------------------------------------- */
  function initFormValidation() {
    var forms = document.querySelectorAll(".needs-validation");
    forms.forEach(function (form) {
      form.addEventListener("submit", function (event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add("was-validated");
      });
    });
  }
 
  /* ---------------------------------------------------------------------
     Copy-to-clipboard helper (used on contact info email row)
     --------------------------------------------------------------------- */
  function initCopyButtons() {
    document.querySelectorAll("[data-copy]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var text = btn.getAttribute("data-copy");
        if (!text) return;
        navigator.clipboard.writeText(text).then(function () {
          var original = btn.innerHTML;
          btn.innerHTML = '<i class="bi bi-check2"></i>';
          setTimeout(function () { btn.innerHTML = original; }, 1400);
        });
      });
    });
  }
 
  document.addEventListener("DOMContentLoaded", function () {
    initTheme();
    initNavbar();
    initHeroTerminal();
    initFormValidation();
    initCopyButtons();
  });
})();


 document.addEventListener('DOMContentLoaded', function() {
    const chatToggleBtn = document.getElementById('chat-toggle-btn');
    const closeChatBtn = document.getElementById('close-chat');
    const chatWindow = document.getElementById('chat-window');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');

    // Generate a simple session ID
    const sessionId = 'session_' + Math.random().toString(36).substr(2, 9);

    // Toggle Chat Window
    function toggleChat() {
        chatWindow.classList.toggle('d-none');
        if (!chatWindow.classList.contains('d-none')) {
            chatInput.focus();
        }
    }

    chatToggleBtn.addEventListener('click', toggleChat);
    closeChatBtn.addEventListener('click', toggleChat);

    // Append Message to UI
    function appendMessage(sender, text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}-message mb-3`;
        
        if (sender === 'user') {
            msgDiv.innerHTML = `<div class="mono small"></div><div class="message-text">${text}</div>`;
        } else {
            msgDiv.innerHTML = `
                <div class="mono small mb-1" style="color: var(--amber);">[system_response]</div>
                <div class="message-text" style="color: #f6f5f1;">${text}</div>
            `;
        }
        
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll
    }

    // Show Typing Indicator
    function showTyping() {
        const typingId = 'typing-' + Date.now();
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message ai-message mb-3';
        typingDiv.id = typingId;
        typingDiv.innerHTML = `
            <div class="mono small mb-1" style="color: var(--amber);">[system_computing]</div>
            <div class="message-text">
                <span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>
            </div>
        `;
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return typingId;
    }

    // Remove Typing Indicator
    function removeTyping(id) {
        const typingDiv = document.getElementById(id);
        if (typingDiv) {
            typingDiv.remove();
        }
    }

    // Handle Form Submit (Sending to FastAPI)
    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const query = chatInput.value.trim();
        if (!query) return;

        // 1. Show user message
        appendMessage('user', query);
        chatInput.value = '';

        // 2. Show typing indicator
        const typingId = showTyping();

        try {
            // 3. Call FastAPI Endpoint
            const response = await fetch('http://localhost:8001/ai/chat/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: sessionId,
                    query: query
                })
            });

            if (!response.ok) throw new Error('API Error');

            const data = await response.json();
            
            // 4. Remove typing indicator & show AI response
            removeTyping(typingId);
            appendMessage('ai', data.reply);

        } catch (error) {
            console.error('Chat Error:', error);
            removeTyping(typingId);
            appendMessage('ai', 'Error: Connection to AI microservice failed. Ensure FastAPI is running on port 8001.');
        }
    });

    // Make sendSuggestedMessage global so inline onclick works
    window.sendSuggestedMessage = function(text) {
        chatInput.value = text;
        chatForm.dispatchEvent(new Event('submit'));
    };
    
});
document.addEventListener('DOMContentLoaded', function() {
    var imageModal = document.getElementById('imageModal');
    if (imageModal) {
        imageModal.addEventListener('show.bs.modal', function (event) {
            // যে ছবিটিতে ক্লিক করা হয়েছে
            var triggerImg = event.relatedTarget; 
            
            // অ্যাট্রিবিউট থেকে ডেটা নেওয়া
            var src = triggerImg.getAttribute('data-img-src');
            var caption = triggerImg.getAttribute('data-img-caption');
            
            // মডালের ভেতরের ছবি এবং ক্যাপশন ট্যাগ সিলেক্ট করা
            var modalImg = imageModal.querySelector('#fullSizeImage');
            var modalCaption = imageModal.querySelector('#fullSizeCaption');
            
            // ডেটা সেট করা
            modalImg.src = src;
            if(caption && caption !== "None") {
                modalCaption.textContent = caption;
            } else {
                modalCaption.textContent = "";
            }
        });
    }
});