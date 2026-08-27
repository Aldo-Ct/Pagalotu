package pe.edu.upeu.orden.dto;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.Getter;
import lombok.Setter;
import pe.edu.upeu.orden.entity.MetodoPago;
import pe.edu.upeu.orden.entity.MomentoPago;
import pe.edu.upeu.orden.entity.TipoComprobante;

import java.util.List;

@Getter
@Setter
public class OrdenRequest {

    @NotNull
    @Positive
    private Long clienteId;

    @NotNull
    private TipoComprobante tipoComprobante;

    @NotNull
    private MetodoPago metodoPago;

    @NotNull
    private MomentoPago momentoPago;

    @NotEmpty
    @Valid
    private List<OrdenDetalleRequest> detalles;
}
