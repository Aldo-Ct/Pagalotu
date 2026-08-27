package pe.edu.upeu.orden.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import pe.edu.upeu.orden.dto.OrdenRequest;
import pe.edu.upeu.orden.dto.OrdenResponse;
import pe.edu.upeu.orden.entity.Orden;
import pe.edu.upeu.orden.entity.OrdenDetalle;
import pe.edu.upeu.orden.exception.ResourceNotFoundException;
import pe.edu.upeu.orden.mapper.OrdenDetalleMapper;
import pe.edu.upeu.orden.mapper.OrdenMapper;
import pe.edu.upeu.orden.repository.OrdenRepository;

import java.math.BigDecimal;
import java.util.List;

@Service
@RequiredArgsConstructor
public class OrdenService {

    private final OrdenRepository ordenRepository;
    private final OrdenMapper ordenMapper;
    private final OrdenDetalleMapper ordenDetalleMapper;

    @Transactional(readOnly = true)
    public List<OrdenResponse> listar() {
        return ordenRepository.findAllConDetalles().stream()
                .map(ordenMapper::toResponse)
                .toList();
    }

    @Transactional(readOnly = true)
    public OrdenResponse obtener(Long id) {
        return ordenMapper.toResponse(buscarOFallar(id));
    }

    @Transactional
    public OrdenResponse crear(OrdenRequest request) {
        Orden orden = ordenMapper.toEntity(request);
        orden.setEstado("PENDIENTE");
        reemplazarDetallesYTotal(orden, request);
        return ordenMapper.toResponse(ordenRepository.save(orden));
    }

    @Transactional
    public OrdenResponse actualizar(Long id, OrdenRequest request) {
        Orden orden = buscarOFallar(id);
        orden.setClienteId(request.getClienteId());
        orden.setTipoComprobante(request.getTipoComprobante());
        orden.setMetodoPago(request.getMetodoPago());
        orden.setMomentoPago(request.getMomentoPago());
        reemplazarDetallesYTotal(orden, request);
        return ordenMapper.toResponse(ordenRepository.save(orden));
    }

    @Transactional
    public void eliminar(Long id) {
        ordenRepository.delete(buscarOFallar(id));
    }

    private Orden buscarOFallar(Long id) {
        return ordenRepository.findByIdConDetalles(id)
                .orElseThrow(() -> new ResourceNotFoundException("Orden no encontrada: " + id));
    }

    private void reemplazarDetallesYTotal(Orden orden, OrdenRequest request) {
        List<OrdenDetalle> detalles = request.getDetalles().stream()
                .map(ordenDetalleMapper::toEntity)
                .toList();
        orden.reemplazarDetalles(detalles);
        BigDecimal total = detalles.stream()
                .map(detalle -> detalle.getPrecioUnitario()
                        .multiply(BigDecimal.valueOf(detalle.getCantidad())))
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        orden.setTotal(total);
    }
}
