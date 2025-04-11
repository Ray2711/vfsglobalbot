def cf_manual_solver(sb) -> None:
    try:
        sb.sleep(3)  # Optional: wait for Cloudflare widget to finish rendering

        sb.driver.execute_script("""
            const iframe = document.querySelector('[id^="cf-chl-widget-"]');
            if (!iframe) throw new Error("❌ CAPTCHA iframe not found");

            const doc = iframe.contentDocument || iframe.contentWindow.document;
            if (!doc) throw new Error("❌ Cannot access iframe document");

            const host = doc.querySelector('challenge-running');
            if (!host) throw new Error("❌ Shadow host not found in iframe");

            const root = host.shadowRoot;
            if (!root) throw new Error("❌ Shadow root not found");

            const checkbox = root.querySelector('input[type="checkbox"]');
            if (!checkbox) throw new Error("❌ Checkbox not found inside shadow root");

            checkbox.click();
        """)

        print("✅ Cloudflare checkbox clicked.")
    except Exception as e:
        print("❌ CAPTCHA solving failed:", e)
