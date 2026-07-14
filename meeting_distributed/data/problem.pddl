
(define (problem meeting-room-problem)

(:domain meeting-room)

(:init
    (room-empty) (light-off) (too-hot) (air-quality-good) (fan-on)
)

(:goal
    (and
        (light-off) (fan-on)
    )
)

)
