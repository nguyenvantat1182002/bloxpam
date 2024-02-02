async function() {
    class bidaithanroblox {
        async register(username, password) {
            const formData = new URLSearchParams();
            formData.append('username', username);
            formData.append('password', password);
            formData.append('password1', password);
    
            const response = await fetch('https://bidaithanroblox.com/login/RegisterUser', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    credentials: 'include'
                },
                body: formData.toString()
            })
            
            return await response.text()
        }
    
        async transaction(serial, id_card, token) {
            const formData = new URLSearchParams();
            formData.append('type', 'VIETTEL');
            formData.append('amount', '500000');
            formData.append('serial', serial);
            formData.append('code', id_card);
            formData.append('token', token);
    
            const response = await fetch('https://bidaithanroblox.com/transaction/index', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    credentials: 'include'
                },
                body: formData.toString()
            })
            
            return await response.text()
        }
    
        encrypt(passphrase, plain_text) {
            var slam_ol = CryptoJS.lib.WordArray.random(256);
            var iv = CryptoJS.lib.WordArray.random(16);
            var key = CryptoJS.PBKDF2(passphrase, slam_ol, {
                hasher: CryptoJS.algo.SHA512,
                keySize: 64 / 8,
                iterations: 999
            });
            var encrypted = CryptoJS.AES.encrypt(plain_text, key, {
                iv: iv
            });
            var data = {
                amtext: CryptoJS.enc.Base64.stringify(encrypted.ciphertext),
                slam_ltol: CryptoJS.enc.Hex.stringify(slam_ol),
                iavmol: CryptoJS.enc.Hex.stringify(iv)
            }
            return JSON.stringify(data);
        }
    
        async transaction2(serial, id_card, token) {
            const formData = new URLSearchParams();
            formData.append('type', 'VIETTEL'); 
            formData.append('amount', '500000');
            formData.append('serial', serial);
            formData.append('code', id_card);
            // formData.append('token', token);
    
            const test_csrf = document.querySelector('input[name=csrf_test_name]').value
            formData.append('csrf_test_name', test_csrf);
    
            // let data = `VIETTEL|500000|${serial}|${id_card}|${token}`
            // data = encrypt('ffffggggggg', data)
    
            const response = await fetch('https://bidaithanroblox.com/transaction/index', {
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
    
    const victim = new bidaithanroblox()
    
    <method>
}