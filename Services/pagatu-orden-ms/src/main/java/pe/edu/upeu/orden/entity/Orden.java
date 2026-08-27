package pe.edu.upeu.orden.entity;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "ordenes")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Orden {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "id_cliente", nullable = false)
    private Long clienteId;

    @Column(name = "fecha_creacion", nullable = false, updatable = false)
    private LocalDateTime fechaCreacion;

    @Column(name = "estado", nullable = false, length = 20)
    private String estado;

    @Enumerated(EnumType.STRING)
    @Column(name = "tipo_comprobante", nullable = false, length = 20)
    private TipoComprobante tipoComprobante;

    @Enumerated(EnumType.STRING)
    @Column(name = "metodo_pago", nullable = false, length = 20)
    private MetodoPago metodoPago;

    @Enumerated(EnumType.STRING)
    @Column(name = "momento_pago", nullable = false, length = 20)
    private MomentoPago momentoPago;

    @Column(name = "total", nullable = false, precision = 10, scale = 2)
    private BigDecimal total;

    @Builder.Default
    @OneToMany(mappedBy = "orden", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<OrdenDetalle> detalles = new ArrayList<>();

    @PrePersist
    void prepararCreacion() {
        if (fechaCreacion == null) {
            fechaCreacion = LocalDateTime.now();
        }
        if (estado == null) {
            estado = "PENDIENTE";
        }
    }

    public void reemplazarDetalles(List<OrdenDetalle> nuevosDetalles) {
        detalles.clear();
        nuevosDetalles.forEach(detalle -> {
            detalle.setOrden(this);
            detalles.add(detalle);
        });
    }
}
