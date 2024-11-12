// Функція для отримання user_id з Telegram Web App API
function getUserIdFromTelegram() {
    if (Telegram.WebApp) {
        const userId = Telegram.WebApp.user.id;  // Отримуємо user_id з Telegram API
        return userId;
    }
    return null;
}

// Функція для відкриття профілю користувача
function openProfile() {
    const userId = getUserIdFromTelegram();  // Отримуємо user_id через Telegram API
    if (userId) {
        fetch(`/get_profile/${userId}`)  
            .then(response => response.json())  // Отримуємо JSON-відповідь від сервера
            .then(data => {
                if (data.error) {
                    alert(data.error);  // Виводимо помилку, якщо користувач не знайдений
                } else {
                    // Виводимо дані користувача на сторінці
                    document.getElementById('profile-info').style.display = 'block';  // Показуємо розділ профілю
                    document.getElementById('username').textContent = "Ім'я: " + data.username;
                    document.getElementById('user-id').textContent = "ID: " + data.user_id;
                    document.getElementById('balance').textContent = "Баланс: " + data.balance + " грн";
                    document.getElementById('level').textContent = "Рівень: " + data.level;
                    document.getElementById('bonus').textContent = "Бонус: " + data.bonus + " год";
                }
            })
            .catch(error => {
                console.error('Помилка при отриманні профілю:', error);
            });
    } else {
        alert("Не вдалося отримати user_id через Telegram API");
    }
}

// Приклад інших функцій для кнопок (Маркет, Канал, Допомога)
function openMarket() {
    window.location.href = "https://www.example.com";
}

function openChannel() {
    window.location.href = "https://t.me/KilorsFilms";  // Замініть на своє посилання
}


function showSupport() {
    window.location.href = "https://t.me/C_ruben";
}


function openProfile() {
    const userId = getUserIdFromURL(); 
    fetch(`/get_profile/${userId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error); 
            } else {
                document.getElementById('profile-info').style.display = 'block';
                document.getElementById('username').textContent = "Ім'я: " + data.username;
                document.getElementById('user-id').textContent = "ID: " + data.user_id;
                document.getElementById('balance').textContent = " " + data.balance + " грн";
                document.getElementById('level').textContent = " " + data.level;
                document.getElementById('bonus').textContent = " " + data.bonus + " H";
            }
        })
        .catch(error => {
            console.error('Помилка при отриманні профілю:', error);
        });
}

// Ініціалізація Telegram Web App
if (Telegram.WebApp) {
    Telegram.WebApp.ready();
    Telegram.WebApp.onEvent('themeChanged', () => {
        // Перевірка чи змінився стиль теми (світла/темна)
    });
}
