let clearedThroughTimestamp = null;


function showTab(tabName) {

    document
        .querySelectorAll(".tab-content")
        .forEach(tab => {

            tab.classList.remove(
                "active-content"
            );

        });


    document
        .querySelectorAll(".nav-button")
        .forEach(button => {

            button.classList.remove(
                "active-tab"
            );

        });


    document
        .getElementById(tabName)
        .classList.add(
            "active-content"
        );


    document
        .getElementById(
            tabName + "-tab"
        )
        .classList.add(
            "active-tab"
        );

}


function setBooleanState(
    elementId,
    state,
    onText,
    offText
) {

    const element =
        document.getElementById(
            elementId
        );


    element.innerText =
        state
            ? onText
            : offText;


    element.className =
        state
            ? "value active"
            : "value inactive";

}


async function updateState() {

    const connection =
        document.getElementById(
            "connection"
        );


    try {

        const response =
            await fetch("/api/state");


        if (!response.ok) {

            throw new Error();

        }


        const state =
            await response.json();


        setBooleanState(
            "occupied",
            state.occupied,
            "OCCUPIED",
            "EMPTY"
        );


        document
            .getElementById(
                "temperature"
            )
            .innerText =

            state.temperature !== null

                ? state.temperature.toFixed(1)
                    + " °C"

                : "Unavailable";


        document
            .getElementById(
                "desired_temperature"
            )
            .innerText =

            state.desired_temperature !== null

                ? state.desired_temperature.toFixed(1)
                    + " °C"

                : "Unavailable";


        document
            .getElementById(
                "humidity"
            )
            .innerText =

            state.humidity !== null

                ? state.humidity.toFixed(1)
                    + " %"

                : "Unavailable";


        document
            .getElementById(
                "air_quality"
            )
            .innerText =
            state.air_quality;


        document
            .getElementById(
                "air_quality_value"
            )
            .innerText =

            "Raw sensor value: "
            + state.air_quality_value;


        document
            .getElementById(
                "rotary_value"
            )
            .innerText =
            state.rotary_value;


        setBooleanState(
            "light",
            state.light,
            "ON",
            "OFF"
        );


        const led =
            document.getElementById(
                "led-visual"
            );


        led.classList.toggle(
            "on",
            state.light
        );


        led.classList.toggle(
            "off",
            !state.light
        );


        setBooleanState(
            "fan",
            state.fan,
            "ON",
            "OFF"
        );


        const fan =
            document.getElementById(
                "fan-visual"
            );


        fan.classList.toggle(
            "spinning",
            state.fan
        );


        connection.innerText =
            "● LIVE";


        connection.className =
            "online";

    }

    catch {

        connection.innerText =
            "● CONNECTION LOST";


        connection.className =
            "offline";

    }

}


async function updateNotifications() {

    try {

        const response =
            await fetch(
                "/api/notifications"
            );


        if (!response.ok) {

            throw new Error();

        }


        const notifications =
            await response.json();


        const list =
            document.getElementById(
                "notification-list"
            );


        const badge =
            document.getElementById(
                "notification-count"
            );


        /*
         * Before Clear View:
         * show all notifications.
         *
         * After Clear View:
         * show only notifications newer than
         * the newest notification that existed
         * when Clear View was clicked.
         */
        const visibleNotifications =

            clearedThroughTimestamp === null

                ? notifications

                : notifications.filter(

                    notification =>

                        notification.timestamp >
                        clearedThroughTimestamp

                );


        badge.innerText =
            visibleNotifications.length;


        if (
            visibleNotifications.length === 0
        ) {

            list.innerHTML =

                `<div class="empty-notifications">
                    Waiting for new notifications...
                 </div>`;

            return;

        }


        list.innerHTML = "";


        visibleNotifications
            .slice()
            .reverse()
            .forEach(notification => {


                const card =
                    document.createElement(
                        "div"
                    );


                card.className =
                    "notification";


                card.innerHTML = `

                    <div class="notification-title">

                        ${notification.action}

                    </div>


                    <div class="notification-message">

                        ${notification.message}

                    </div>


                    <div class="notification-time">

                        ${notification.timestamp}

                    </div>

                `;


                list.appendChild(card);

            });

    }

    catch {

        console.log(
            "Notification update failed"
        );

    }

}


async function clearNotificationView() {

    try {

        const response =
            await fetch(
                "/api/notifications"
            );


        if (!response.ok) {

            throw new Error();

        }


        const notifications =
            await response.json();


        /*
         * Remember the newest notification
         * that currently exists.
         */
        if (
            notifications.length > 0
        ) {

            clearedThroughTimestamp =

                notifications[
                    notifications.length - 1
                ].timestamp;

        }


        document
            .getElementById(
                "notification-count"
            )
            .innerText = 0;


        document
            .getElementById(
                "notification-list"
            )
            .innerHTML =

            `<div class="empty-notifications">
                Notification view cleared.
             </div>`;

    }

    catch {

        console.log(
            "Failed to clear notification view"
        );

    }

}


/*
 * Initial dashboard loading.
 */

updateState();

updateNotifications();


/*
 * Update room state every second.
 */

setInterval(
    updateState,
    1000
);


/*
 * Check for new notifications every second.
 */

setInterval(
    updateNotifications,
    1000
);