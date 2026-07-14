(define (domain meeting-room)

    (:requirements :strips)

    (:predicates

        (occupied)
        (room-empty)

        (light-on)
        (light-off)

        (fan-on)
        (fan-off)

        (too-hot)
        (comfortable)

        (air-quality-good)
        (air-quality-poor)
    )

    ;; -----------------------
    ;; LIGHT
    ;; -----------------------

    (:action switch-light-on

        :parameters ()

        :precondition
            (and
                (occupied)
                (light-off)
            )

        :effect
            (and
                (light-on)
                (not (light-off))
            )
    )

    (:action switch-light-off

        :parameters ()

        :precondition
            (and
                (room-empty)
                (light-on)
            )

        :effect
            (and
                (light-off)
                (not (light-on))
            )
    )

    ;; -----------------------
    ;; FAN
    ;; -----------------------

    (:action switch-fan-on

        :parameters ()

        :precondition
            (and
                (fan-off)
            )

        :effect
            (and
                (fan-on)
                (not (fan-off))
            )
    )

    (:action switch-fan-off

        :parameters ()

        :precondition
            (and
                (fan-on)
            )

        :effect
            (and
                (fan-off)
                (not (fan-on))
            )
    )

)