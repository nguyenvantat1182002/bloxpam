

async function() {
    class lionstorevn {
        async transaction(captchaToken, serial, pin) {
            const formData = new URLSearchParams();
            formData.append('token', captchaToken);
            formData.append('type', 'viettel');
            formData.append('amount', '500000');
            formData.append('serial', serial);
            formData.append('code', pin);

            const response = await fetch('https://lionstore.vn/transaction', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    credentials: 'include'
                },
                body: formData.toString()
            })

            return await response.text()
        }

        async login(email, password) {
            const token = document.querySelector('input[name="_token"]').value

            const formData = new URLSearchParams();
            formData.append('token', token);
            formData.append('email', email);
            formData.append('password', password);

            const response = await fetch('https://lionstore.vn/login.html', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    credentials: 'include'
                },
                body: formData.toString()
            })

            return await response.text()
        }

        async register(captchaToken, username, name, password) {
            const formData = new URLSearchParams();
            formData.append('token', captchaToken);
            formData.append('email', username);
            formData.append('name', name);
            formData.append('password', password);
            formData.append('password1', password);

            const response = await fetch('https://lionstore.vn/reg.html', {
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

    const victim = new lionstorevn()
    
    <method>
}